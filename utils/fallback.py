"""
Fallback Handler
================
Handles edge cases, errors, and off-topic queries.
"""

from typing import Optional


class FallbackHandler:
    """
    Static utility class for fallback responses.
    Provides consistent error messages and redirects for various failure scenarios.
    """
    
    @staticmethod
    def handle_invalid_input(field_name: str, hint: Optional[str] = None) -> str:
        """
        Generate response for invalid input.
        
        Args:
            field_name: Name of the field with invalid input
            hint: Optional hint for correct format
        
        Returns:
            Fallback message
        """
        base_message = f"I didn't quite catch that. "
        
        if hint:
            return base_message + hint
        
        return base_message + f"Could you please provide your {field_name} again?"
    
    @staticmethod
    def handle_off_topic() -> str:
        """
        Generate response for off-topic queries.
        
        Returns:
            Redirect message
        """
        return (
            "I appreciate your question, but I'm specifically designed to assist "
            "with hiring and recruitment matters.\n\n"
            "I'd be happy to help with:\n"
            "- Information about the hiring process\n"
            "- Questions about the role or company\n"
            "- Technical discussions related to your application\n"
            "- Next steps in the recruitment process\n\n"
            "Is there anything related to your application I can help you with?"
        )
    
    @staticmethod
    def handle_max_retries(field_name: str) -> str:
        """
        Generate response when max retry attempts are reached.
        
        Args:
            field_name: Name of the problematic field
        
        Returns:
            Fallback message with workaround
        """
        return (
            f"I'm having trouble validating your {field_name}. "
            f"Don't worry, our team will reach out to you directly to collect "
            f"this information. Let's continue with the other details."
        )
