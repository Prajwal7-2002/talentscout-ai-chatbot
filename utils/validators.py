"""
Input Validators
================
Validation utilities for candidate information.
"""

import re
from config import Config


class Validators:
    """Static utility class for input validation."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
        
        Returns:
            True if email format is valid
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.strip()))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate phone number format.
        
        Args:
            phone: Phone number to validate
        
        Returns:
            True if phone format is valid (10+ digits)
        """
        # Extract only digits
        digits = re.sub(r'\D', '', phone)
        return len(digits) >= 10
    
    @staticmethod
    def validate_experience(experience: str) -> bool:
        """
        Validate years of experience input.
        
        Args:
            experience: Experience input (can be number or range)
        
        Returns:
            True if experience is valid
        """
        # Try to extract first number from the string
        numbers = re.findall(r'\d+', experience.strip())
        
        if not numbers:
            return False
        
        try:
            years = int(numbers[0])
            return Config.MIN_EXPERIENCE_YEARS <= years <= Config.MAX_EXPERIENCE_YEARS
        except (ValueError, IndexError):
            return False
