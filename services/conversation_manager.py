"""
Conversation State Manager
===========================
State machine for managing conversation flow and data collection.
"""

from enum import Enum
from typing import Dict, Any, List
from datetime import datetime

from config import Config
from services.llm_service import LLMService
from utils.validators import Validators
from utils.fallback import FallbackHandler
from prompts.system_prompt import SYSTEM_PROMPT
from prompts.info_collection_prompt import INFO_COLLECTION_PROMPTS
from prompts.question_generation_prompt import QUESTION_GENERATION_PROMPT


class ConversationState(Enum):
    """Enumeration of conversation states."""
    GREETING = "greeting"
    COLLECTING_NAME = "collecting_name"
    COLLECTING_EMAIL = "collecting_email"
    COLLECTING_PHONE = "collecting_phone"
    COLLECTING_EXPERIENCE = "collecting_experience"
    COLLECTING_POSITION = "collecting_position"
    COLLECTING_LOCATION = "collecting_location"
    COLLECTING_TECH_STACK = "collecting_tech_stack"
    GENERATING_QUESTIONS = "generating_questions"
    COMPLETED = "completed"


class ConversationManager:
    """
    Manages conversation state, candidate data, and response generation.
    
    Implements a state machine approach for structured information collection.
    """
    
    def __init__(self, llm_service: LLMService):
        """Initialize conversation manager."""
        self.llm_service = llm_service
        self.state = ConversationState.GREETING
        self.candidate_data: Dict[str, Any] = {
            "name": None,
            "email": None,
            "phone": None,
            "experience": None,
            "position": None,
            "location": None,
            "tech_stack": None,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history: List[Dict[str, str]] = []
        self.retry_count = 0
        self.max_retries = 3
    
    def get_initial_greeting(self) -> str:
        """Generate the initial greeting message."""
        greeting = (
            "Hello! I'm TalentScout, your AI hiring assistant.\n\n"
            "I'm here to learn more about you and your technical background. "
            "This will be a brief conversation where I'll collect some information "
            "and generate personalized technical questions based on your expertise.\n\n"
            "**Privacy Notice:** Your information will be stored securely and used solely "
            "for recruitment purposes. By continuing, you consent to our data collection "
            "practices as outlined in our privacy policy.\n\n"
            "Let's get started! What's your full name?"
        )
        self.state = ConversationState.COLLECTING_NAME
        return greeting
    
    def process_message(self, user_message: str) -> str:
        """
        Process user message based on current conversation state.
        
        Args:
            user_message: User's input message
        
        Returns:
            Assistant's response
        """
        # Route to appropriate handler based on state
        if self.state == ConversationState.COLLECTING_NAME:
            return self._handle_name_collection(user_message)
        elif self.state == ConversationState.COLLECTING_EMAIL:
            return self._handle_email_collection(user_message)
        elif self.state == ConversationState.COLLECTING_PHONE:
            return self._handle_phone_collection(user_message)
        elif self.state == ConversationState.COLLECTING_EXPERIENCE:
            return self._handle_experience_collection(user_message)
        elif self.state == ConversationState.COLLECTING_POSITION:
            return self._handle_position_collection(user_message)
        elif self.state == ConversationState.COLLECTING_LOCATION:
            return self._handle_location_collection(user_message)
        elif self.state == ConversationState.COLLECTING_TECH_STACK:
            return self._handle_tech_stack_collection(user_message)
        elif self.state == ConversationState.COMPLETED:
            return self._handle_completed_state(user_message)
        
        return "I'm not sure how to help with that. Could you please try again?"
    
    def _handle_name_collection(self, user_message: str) -> str:
        """Handle name collection state."""
        name = user_message.strip()
        if len(name) < 2:
            return FallbackHandler.handle_invalid_input("name", "Please provide your full name.")
        
        self.candidate_data["name"] = name
        self.state = ConversationState.COLLECTING_EMAIL
        return INFO_COLLECTION_PROMPTS["email"].format(name=name)
    
    def _handle_email_collection(self, user_message: str) -> str:
        """Handle email collection state with validation."""
        email = user_message.strip()
        
        if not Validators.validate_email(email):
            self.retry_count += 1
            if self.retry_count >= self.max_retries:
                self.retry_count = 0
                return FallbackHandler.handle_max_retries("email")
            return FallbackHandler.handle_invalid_input(
                "email",
                "Please provide a valid email address (e.g., name@example.com)."
            )
        
        self.candidate_data["email"] = email
        self.retry_count = 0
        self.state = ConversationState.COLLECTING_PHONE
        return INFO_COLLECTION_PROMPTS["phone"]
    
    def _handle_phone_collection(self, user_message: str) -> str:
        """Handle phone collection state with validation."""
        phone = user_message.strip()
        
        if not Validators.validate_phone(phone):
            self.retry_count += 1
            if self.retry_count >= self.max_retries:
                self.retry_count = 0
                return FallbackHandler.handle_max_retries("phone")
            return FallbackHandler.handle_invalid_input(
                "phone",
                "Please provide a valid phone number (10+ digits)."
            )
        
        self.candidate_data["phone"] = phone
        self.retry_count = 0
        self.state = ConversationState.COLLECTING_EXPERIENCE
        return INFO_COLLECTION_PROMPTS["experience"]
    
    def _handle_experience_collection(self, user_message: str) -> str:
        """Handle experience collection state with validation."""
        experience = user_message.strip()
        
        if not Validators.validate_experience(experience):
            self.retry_count += 1
            if self.retry_count >= self.max_retries:
                self.retry_count = 0
                return FallbackHandler.handle_max_retries("experience")
            return FallbackHandler.handle_invalid_input(
                "experience",
                "Please provide a valid number of years (0-50)."
            )
        
        self.candidate_data["experience"] = experience
        self.retry_count = 0
        self.state = ConversationState.COLLECTING_POSITION
        return INFO_COLLECTION_PROMPTS["position"]
    
    def _handle_position_collection(self, user_message: str) -> str:
        """Handle position collection state."""
        position = user_message.strip()
        if len(position) < 2:
            return FallbackHandler.handle_invalid_input(
                "position",
                "Please specify the position(s) you're interested in."
            )
        
        self.candidate_data["position"] = position
        self.state = ConversationState.COLLECTING_LOCATION
        return INFO_COLLECTION_PROMPTS["location"]
    
    def _handle_location_collection(self, user_message: str) -> str:
        """Handle location collection state."""
        location = user_message.strip()
        if len(location) < 2:
            return FallbackHandler.handle_invalid_input(
                "location",
                "Please provide your current location."
            )
        
        self.candidate_data["location"] = location
        self.state = ConversationState.COLLECTING_TECH_STACK
        return INFO_COLLECTION_PROMPTS["tech_stack"]
    
    def _handle_tech_stack_collection(self, user_message: str) -> str:
        """Handle tech stack collection and trigger question generation."""
        tech_stack = user_message.strip()
        if len(tech_stack) < 2:
            return FallbackHandler.handle_invalid_input(
                "tech_stack",
                "Please list the technologies you're proficient in."
            )
        
        self.candidate_data["tech_stack"] = tech_stack
        self.state = ConversationState.GENERATING_QUESTIONS
        
        # Parse tech stack into list
        tech_list = [tech.strip() for tech in tech_stack.split(",")]
        
        # Generate technical questions
        questions = self.llm_service.generate_technical_questions(
            tech_list,
            QUESTION_GENERATION_PROMPT
        )
        
        self.state = ConversationState.COMPLETED
        
        response = (
            f"Excellent! Thank you for sharing your tech stack.\n\n"
            f"Based on your expertise in **{tech_stack}**, here are some "
            f"technical questions our team would like to discuss with you:\n\n"
            f"{questions}\n\n"
            f"---\n\n"
            f"That completes the initial screening! Your information has been recorded. "
            f"Our hiring team will review your profile and reach out soon to schedule "
            f"a technical interview.\n\n"
            f"Feel free to type 'exit' if you'd like to end the conversation, or ask "
            f"any questions you might have about the role or process."
        )
        
        return response
    
    def _handle_completed_state(self, user_message: str) -> str:
        """Handle messages after information collection is complete."""
        response = self.llm_service.generate_response(
            system_prompt=SYSTEM_PROMPT,
            user_message=user_message,
            conversation_history=self.conversation_history[-6:]
        )
        
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def get_candidate_data(self) -> Dict[str, Any]:
        """Retrieve collected candidate data."""
        return self.candidate_data.copy()
