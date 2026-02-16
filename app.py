"""
TalentScout AI Hiring Assistant - Main Application
===================================================
Production-grade Streamlit application for AI-powered candidate screening.
"""

import streamlit as st
from typing import Dict, Any, List
import json
from pathlib import Path
from datetime import datetime
import uuid

from config import Config
from services.conversation_manager import ConversationManager
from services.llm_service import LLMService


def load_conversations() -> Dict[str, Any]:
    """Load conversations from disk if they exist."""
    conversations_file = Path(Config.DATA_DIR) / "conversations.json"
    
    if conversations_file.exists():
        try:
            with open(conversations_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Convert back to conversation managers
                for conv_id, conv_data in data.items():
                    # Recreate LLM service and conversation manager
                    conv_data["conversation_manager"] = ConversationManager(st.session_state.llm_service)
                    # Restore state from saved data
                    if "candidate_data" in conv_data:
                        conv_data["conversation_manager"].candidate_data = conv_data["candidate_data"]
                    if "state" in conv_data:
                        conv_data["conversation_manager"].state = conv_data["state"]
                return data
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error loading conversations: {e}")
            return {}
    return {}


def save_conversations() -> None:
    """Save current conversations to disk."""
    conversations_file = Path(Config.DATA_DIR) / "conversations.json"
    
    # Prepare data for serialization
    serializable_convs = {}
    for conv_id, conv_data in st.session_state.conversations.items():
        manager = conv_data["conversation_manager"]
        serializable_convs[conv_id] = {
            "id": conv_data["id"],
            "messages": conv_data["messages"],
            "created_at": conv_data["created_at"],
            "title": conv_data["title"],
            "awaiting_input": conv_data["awaiting_input"],
            "candidate_data": manager.candidate_data,
            "state": manager.state.value if hasattr(manager.state, 'value') else str(manager.state)
        }
    
    try:
        with open(conversations_file, "w", encoding="utf-8") as f:
            json.dump(serializable_convs, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving conversations: {e}")


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "llm_service" not in st.session_state:
        st.session_state.llm_service = LLMService(api_key=Config.GROQ_API_KEY)
    
    if "conversations" not in st.session_state:
        # Try to load from disk first
        st.session_state.conversations = load_conversations()
    
    if "current_conversation_id" not in st.session_state:
        st.session_state.current_conversation_id = None


def create_new_conversation() -> str:
    """Create a new conversation and return its ID."""
    conversation_id = str(uuid.uuid4())
    
    st.session_state.conversations[conversation_id] = {
        "id": conversation_id,
        "messages": [],
        "conversation_manager": ConversationManager(st.session_state.llm_service),
        "created_at": datetime.now().isoformat(),
        "title": "New Conversation",
        "awaiting_input": True
    }
    
    return conversation_id


def get_current_conversation() -> Dict[str, Any]:
    """Get the current active conversation."""
    if st.session_state.current_conversation_id is None:
        # Create first conversation
        conv_id = create_new_conversation()
        st.session_state.current_conversation_id = conv_id
    
    return st.session_state.conversations[st.session_state.current_conversation_id]


def render_sidebar() -> None:
    """Render the sidebar with conversation history."""
    with st.sidebar:
        st.title("Conversations")
        
        # New Chat button
        if st.button("+ New Chat", use_container_width=True):
            conv_id = create_new_conversation()
            st.session_state.current_conversation_id = conv_id
            st.rerun()
        
        st.divider()
        
        # List all conversations (most recent first)
        sorted_convs = sorted(
            st.session_state.conversations.items(),
            key=lambda x: x[1]["created_at"],
            reverse=True
        )
        
        if sorted_convs:
            st.subheader("History")
            for conv_id, conv_data in sorted_convs:
                # Show conversation title
                title = conv_data["title"]
                is_current = conv_id == st.session_state.current_conversation_id
                
                # Highlight current conversation
                button_label = f"{'> ' if is_current else ''}{title}"
                
                if st.button(
                    button_label,
                    key=f"conv_{conv_id}",
                    use_container_width=True,
                    type="primary" if is_current else "secondary"
                ):
                    st.session_state.current_conversation_id = conv_id
                    st.rerun()
        else:
            st.info("No conversations yet. Start chatting!")
        
        st.divider()
        
        # Stats
        total_convs = len(st.session_state.conversations)
        st.caption(f"Total Conversations: {total_convs}")


def display_chat_history() -> None:
    """Render the complete chat history in the Streamlit UI."""
    conv = get_current_conversation()
    for message in conv["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input(user_message: str) -> None:
    """Process user input and generate appropriate responses."""
    conv = get_current_conversation()
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_message)
    conv["messages"].append({"role": "user", "content": user_message})
    
    # Check for exit keywords
    if user_message.lower().strip() in Config.EXIT_KEYWORDS:
        handle_exit()
        return
    
    # Process message through conversation manager
    manager: ConversationManager = conv["conversation_manager"]
    response = manager.process_message(user_message)
    
    # Update conversation title based on candidate name
    if manager.candidate_data.get("name") and conv["title"] == "New Conversation":
        conv["title"] = f"{manager.candidate_data['name']}"
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    conv["messages"].append({"role": "assistant", "content": response})


def handle_exit() -> None:
    """Handle graceful exit: save candidate data and display farewell message."""
    conv = get_current_conversation()
    manager: ConversationManager = conv["conversation_manager"]
    
    # Save candidate data to JSON
    candidate_data = manager.get_candidate_data()
    if candidate_data.get("name"):
        save_candidate_data(candidate_data)
    
    # Display exit message
    exit_message = (
        "Thank you for your time! Your information has been saved. "
        "Our team will review your application and get back to you soon. "
        "Have a great day!"
    )
    
    with st.chat_message("assistant"):
        st.markdown(exit_message)
    conv["messages"].append({"role": "assistant", "content": exit_message})
    
    # Update conversation title if we have a name
    if candidate_data.get("name"):
        conv["title"] = f"{candidate_data['name']} [Complete]"
    
    # Disable further input
    conv["awaiting_input"] = False


def save_candidate_data(candidate_data: Dict[str, Any]) -> None:
    """Persist candidate data to local JSON storage."""
    data_file = Path(Config.DATA_FILE_PATH)
    
    # Load existing data
    existing_data = []
    if data_file.exists():
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []
    
    # Append new candidate
    existing_data.append(candidate_data)
    
    # Save updated data
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)


def initialize_conversation() -> None:
    """Start the conversation with an initial greeting if no messages exist."""
    conv = get_current_conversation()
    
    if len(conv["messages"]) == 0:
        manager: ConversationManager = conv["conversation_manager"]
        greeting = manager.get_initial_greeting()
        
        with st.chat_message("assistant"):
            st.markdown(greeting)
        conv["messages"].append({"role": "assistant", "content": greeting})


def main() -> None:
    """Main application entry point."""
    # Page configuration
    st.set_page_config(
        page_title="TalentScout AI | Hiring Assistant",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar with conversation history
    render_sidebar()
    
    # Main chat area
    st.title("TalentScout AI")
    st.markdown("### Your Intelligent Hiring Assistant")
    st.markdown("---")
    
    # Display chat history
    display_chat_history()
    
    # Initialize conversation with greeting
    initialize_conversation()
    
    # Get current conversation
    conv = get_current_conversation()
    
    # Chat input
    if conv["awaiting_input"]:
        if user_input := st.chat_input("Type your message here..."):
            handle_user_input(user_input)
            st.rerun()
    else:
        st.info("Session ended. Click 'New Chat' in the sidebar to start a new conversation.")


if __name__ == "__main__":
    main()
