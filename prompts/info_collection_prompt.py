"""
Information Collection Prompts
===============================
Templated prompts for structured information gathering.
"""

INFO_COLLECTION_PROMPTS = {
    "email": (
        "Great to meet you, {name}!\n\n"
        "Could you please provide your email address? This will be our primary "
        "channel for communication regarding your application."
    ),
    
    "phone": (
        "Thank you!\n\n"
        "Next, could you share your phone number? We'll use this as a backup "
        "contact method."
    ),
    
    "experience": (
        "Perfect!\n\n"
        "How many years of professional experience do you have in software development "
        "or your relevant field? You can provide a number or approximate range, for example '3' or '2-3'."
    ),
    
    "position": (
        "Got it!\n\n"
        "What position or positions are you interested in applying for? Feel free to mention "
        "multiple roles if applicable, such as 'Backend Developer' or 'Full Stack Engineer'."
    ),
    
    "location": (
        "Excellent!\n\n"
        "Where are you currently located? Please provide your City, State, or Country."
    ),
    
    "tech_stack": (
        "Almost done!\n\n"
        "Please list the technologies, programming languages, and frameworks you're "
        "proficient in. Separate them with commas.\n\n"
        "For example: Python, Django, PostgreSQL, Docker, AWS"
    )
}
