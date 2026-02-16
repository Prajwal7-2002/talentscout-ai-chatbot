"""
LLM Service Layer
=================
Abstraction layer for Groq API interactions.
"""

from typing import List, Dict, Optional
from groq import Groq

from config import Config


class LLMService:
    """Service class for LLM interactions using Groq."""
    
    def __init__(self, api_key: str):
        """Initialize LLM service with Groq API credentials."""
        self.client = Groq(api_key=api_key)
        self.model = Config.MODEL_NAME
        self.temperature = Config.TEMPERATURE
        self.max_tokens = Config.MAX_TOKENS
    
    def generate_response(
        self,
        system_prompt: str,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            system_prompt: System-level instructions
            user_message: Current user message
            conversation_history: Prior conversation (optional)
        
        Returns:
            Generated response from the LLM
        """
        messages = [{"role": "system", "content": system_prompt}]
        
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"LLM API Error: {str(e)}")
            return (
                "I apologize, but I'm experiencing technical difficulties. "
                "Could you please repeat that?"
            )
    
    def generate_technical_questions(
        self,
        tech_stack: List[str],
        question_generation_prompt: str
    ) -> str:
        """
        Generate technical questions based on candidate's tech stack.
        
        Args:
            tech_stack: List of technologies
            question_generation_prompt: Template prompt
        
        Returns:
            Generated technical questions
        """
        tech_list = ", ".join(tech_stack)
        user_prompt = question_generation_prompt.format(tech_stack=tech_list)
        
        system_prompt = (
            "You are an expert technical interviewer. Generate high-quality "
            "technical questions that assess both theoretical knowledge and "
            "practical problem-solving skills."
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Question Generation Error: {str(e)}")
            return (
                "I apologize, but I'm having trouble generating questions "
                "at the moment. Our team will prepare questions manually "
                "based on your tech stack."
            )
