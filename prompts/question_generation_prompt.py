"""
Question Generation Prompt
===========================
Template for generating technical interview questions.
"""

QUESTION_GENERATION_PROMPT = """Generate 3-5 high-quality technical interview questions based on the following tech stack:

**Tech Stack:** {tech_stack}

REQUIREMENTS:
1. Generate 3-5 questions total, distributed across the technologies mentioned.
2. Each technology should have at least one question if possible.
3. Avoid basic definition questions (e.g., "What is Python?").
4. Include at least one scenario-based or problem-solving question per technology.
5. Questions should assess both theoretical understanding and practical application.
6. Difficulty should be intermediate level.

FORMAT:
Group questions by technology clearly. Use the following format:

### Technology Name
1. Question text here
2. Another question text

### Another Technology
1. Question text here

FOCUS AREAS:
- Practical problem-solving
- Best practices and design patterns
- Real-world scenarios
- System design considerations
- Performance and optimization
- Common pitfalls and debugging

Generate comprehensive, insightful questions that will help assess the candidate's expertise."""
