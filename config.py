"""
Configuration Management
========================
Centralized configuration for TalentScout application.
"""

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Centralized configuration class."""
    
    # Groq API Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME: str = "llama-3.1-8b-instant"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 500
    
    # Data Storage
    DATA_DIR: Path = Path(__file__).parent / "data"
    DATA_FILE_PATH: Path = DATA_DIR / "candidates.json"
    
    # Exit Keywords
    EXIT_KEYWORDS: List[str] = ["exit", "quit", "bye", "stop"]
    
    # Required Fields (in collection order)
    REQUIRED_FIELDS: List[str] = [
        "name", "email", "phone", "experience",
        "position", "location", "tech_stack"
    ]
    
    # Validation Settings
    MIN_EXPERIENCE_YEARS: int = 0
    MAX_EXPERIENCE_YEARS: int = 50
    
    @classmethod
    def validate(cls) -> None:
        """Validate critical configuration on startup."""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY not found. Set it in environment variables."
            )
        
        # Ensure data directory exists
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
