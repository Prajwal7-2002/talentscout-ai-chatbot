# TalentScout AI - Hiring Assistant Chatbot

An intelligent chatbot that streamlines the candidate screening process by collecting structured information and generating personalized technical interview questions.

---

## What Does It Do?

TalentScout automates the initial stages of technical recruitment. Instead of manually collecting candidate information through forms or emails, this chatbot conducts a natural conversation to gather everything you need:

- Candidate's contact information and background
- Technical expertise and experience level
- Position preferences and location
- Technology stack proficiency

Once the information is collected, it uses AI to generate custom technical interview questions tailored to each candidate's specific tech stack. No two candidates get the same generic questions - each interview is personalized.

---

## Key Features

**Smart Information Collection**
- Conversational flow that feels natural, not like filling out a form
- Real-time validation for emails, phone numbers, and experience years
- Retry logic with helpful hints when users make mistakes

**AI-Powered Question Generation**
- Generates 3-5 technical questions for each technology mentioned
- Questions focus on practical scenarios, not theoretical definitions
- Intermediate difficulty level to properly assess candidates

**Robust Error Handling**
- Graceful fallbacks when validation fails
- Won't let users drift off-topic during screening
- Clear exit options at any point in the conversation

**Conversation Management**
- ChatGPT-style sidebar with conversation history
- Switch between multiple candidate conversations
- Each conversation gets auto-named after the candidate

---

## How to Run It

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` - for the chat interface
- `groq` - for AI-powered responses
- `python-dotenv` - for managing your API key

### Step 2: Get Your Free Groq API Key

1. Visit https://console.groq.com/
2. Sign up (no credit card required)
3. Navigate to "API Keys" in the sidebar
4. Click "Create API Key" and copy it

### Step 3: Configure Your Environment

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_api_key_here
```

Or set it directly in your terminal:

```bash
# Windows PowerShell
$env:GROQ_API_KEY="your_api_key_here"

# Linux/Mac
export GROQ_API_KEY="your_api_key_here"
```

### Step 4: Launch the App

```bash
streamlit run app.py
```

The chatbot will open in your browser at `http://localhost:8501`

---

## Project Architecture

The codebase follows clean architecture principles with clear separation of concerns:

```
app.py                  # UI layer - handles Streamlit interface
├── services/
│   ├── conversation_manager.py   # Brain - manages state machine
│   └── llm_service.py             # AI integration - talks to Groq
├── prompts/
│   ├── system_prompt.py           # Defines chatbot personality
│   ├── info_collection_prompt.py  # Questions for each field
│   └── question_generation_prompt.py  # Instructions for question AI
├── utils/
│   ├── validators.py              # Input validation logic
│   └── fallback.py                # Error message templates
├── config.py                      # All settings in one place
└── data/
    └── candidates.json            # Local storage for candidate data
```

**Why this structure?**
- Easy to update prompts without touching code
- Swap AI providers by only changing the service layer
- Validators are reusable across projects
- Configuration changes don't require code edits

---

## How It Works Internally

### The Conversation Flow

```
User opens app
    ↓
Greeting + first question (name)
    ↓
Collect 7 fields sequentially:
  - Name
  - Email (with validation)
  - Phone (with validation)
  - Years of experience (0-50 range)
  - Desired position(s)
  - Current location
  - Tech stack
    ↓
Send tech stack to AI
    ↓
AI generates personalized questions
    ↓
Display questions + completion message
    ↓
Open-ended conversation (ask about role, etc.)
    ↓
User types "exit" to end
    ↓
Save all data to JSON
```

### State Machine Design

The conversation uses a state machine to ensure a structured flow:

```python
GREETING → COLLECTING_NAME → COLLECTING_EMAIL → COLLECTING_PHONE 
→ COLLECTING_EXPERIENCE → COLLECTING_POSITION → COLLECTING_LOCATION 
→ COLLECTING_TECH_STACK → GENERATING_QUESTIONS → COMPLETED
```

Each state knows exactly what to expect from the user and what to ask next. This prevents the conversation from becoming chaotic.

---

## Prompt Engineering Strategy

### System Prompt
Defines the chatbot's role and boundaries. It explicitly states:
- "You are ONLY a hiring assistant" (prevents off-topic conversations)
- Professional but friendly tone
- When to be strict (during collection) vs. flexible (post-collection)

### Information Collection Prompts
Each field has a carefully crafted prompt that:
- Uses the candidate's name for personalization
- Explains WHY we're asking for the information
- Provides format examples for complex fields
- Maintains a conversational tone

### Question Generation Prompt
Instructs the AI to:
- Generate 3-5 questions per technology
- Focus on scenarios, not definitions
- Use intermediate difficulty
- Group questions by technology for readability

**Why separate prompts from code?**
Non-technical stakeholders (recruiters, HR) can iterate on conversation flow without needing a developer. Prompts are version-controlled separately from business logic.

---

## Configuration Options

Edit `config.py` to customize behavior:

```python
MODEL_NAME = "llama-3.1-8b-instant"  # Groq model to use
TEMPERATURE = 0.7                     # Response creativity (0-1)
MAX_TOKENS = 500                      # Response length limit
EXIT_KEYWORDS = ["exit", "quit", "bye", "stop"]  # Trigger words
```

**Model Options on Groq:**
- `llama-3.1-8b-instant` - Fastest, recommended for chat
- `mixtral-8x7b-32768` - Good balance of speed and quality
- `llama-3.3-70b-versatile` - Highest quality, slower

---

## Data Privacy Considerations

**Current Implementation:**
- Stores candidate data in local `candidates.json` file
- No encryption at rest
- No cloud transmission (except to Groq for question generation)
- `.gitignore` prevents accidental commits

**For Production Use:**
- Encrypt `candidates.json` with AES-256
- Use a proper database (PostgreSQL/MongoDB)
- Implement data retention policies (auto-delete after 30 days)
- Add GDPR consent checkboxes
- Use environment-specific encryption keys
- Implement audit logging for data access

---

## Technical Decisions Explained

### Why Streamlit?
- Built-in chat components (`st.chat_message`, `st.chat_input`)
- No need for separate frontend/backend
- Session state management out of the box
- Perfect for rapid prototyping

### Why Groq Instead of OpenAI?
- Free tier with no credit card requirement
- 10-100x faster inference
- Good enough quality for this use case
- Easier for assignment submission (no billing setup)

### Why State Machine Pattern?
- Prevents spaghetti code with nested if statements
- Makes conversation flow explicit and testable
- Easy to add/remove collection fields
- Clear error handling for each state

### Why Separate Validators?
- Reusable across different projects
- Easy to unit test in isolation
- Can swap validation rules without touching conversation logic
- Centralized error message formatting

---

## Challenges Faced During Development

### Challenge 1: Streamlit Session Persistence
**Problem:** Streamlit reruns the entire script on every user interaction, which would normally lose all conversation state.

**Solution:** Used `st.session_state` to persist the conversation manager, message history, and current state across reruns.

### Challenge 2: LLM API Reliability
**Problem:** API calls can fail due to network issues, rate limits, or service outages.

**Solution:** Wrapped all LLM calls in try-except blocks with meaningful fallback messages. The app continues to function even if question generation fails - it just notifies the user that questions will be prepared manually.

### Challenge 3: Input Validation Edge Cases
**Problem:** Users enter creative variations (email with emojis, phone numbers with spaces/dashes, experience as ranges like "2-3 years").

**Solution:** 
- Email: RFC 5322-compliant regex that handles international domains
- Phone: Accept any format with 10+ digits, strip non-numeric characters
- Experience: Accept numeric strings, validate range 0-50
- Retry limit of 3 attempts before fallback to manual collection

### Challenge 4: Tech Stack Parsing
**Problem:** Users format tech stacks differently ("Python, Django" vs "Python/Django/PostgreSQL" vs "Python Django AWS").

**Solution:** Split by commas, strip whitespace, and let the LLM handle variations. The AI is smart enough to understand different formatting.

---

## Future Enhancements

**Short Term:**
- Resume upload and parsing (extract tech stack automatically)
- Email notifications when candidate completes screening
- Export candidates to CSV for ATS integration

**Medium Term:**
- Admin dashboard to review candidates
- Question difficulty levels (junior/mid/senior)
- Multi-language support (Spanish, French, etc.)

**Long Term:**
- Integration with major ATS platforms (Greenhouse, Lever)
- Voice-based screening (speech-to-text)
- Coding challenge integration (HackerRank, LeetCode)

---

## Assignment Requirements Checklist

✅ **Greeting:** Welcomes candidates and explains the process  
✅ **Information Gathering:** Collects all 7 required fields  
✅ **Tech Stack Declaration:** Accepts comma-separated technologies  
✅ **Technical Question Generation:** Creates 3-5 questions per technology using AI  
✅ **Context Handling:** Maintains conversation history for follow-up questions  
✅ **Fallback Mechanism:** Handles invalid input and off-topic queries  
✅ **Exit Conversation:** Gracefully ends on keywords (exit, quit, bye, stop)  
✅ **Clean UI:** Streamlit interface with chat-style interactions  
✅ **Prompt Engineering:** Separate prompt files with clear instructions  
✅ **Data Privacy:** Local storage with security recommendations  
✅ **Documentation:** Comprehensive README with setup and architecture  

---

## Libraries and Technologies

| Library | Version | Purpose |
|---------|---------|---------|
| Streamlit | 1.31.0 | Frontend chat interface |
| Groq | Latest | AI model API client |
| Python-dotenv | 1.0.1 | Environment variable management |

**Model Details:**
- Provider: Groq (https://groq.com)
- Model: Llama 3.1 8B Instant
- Context: 8192 tokens
- Temperature: 0.7 (balanced creativity)
- Max tokens: 500 for collection, 800 for questions

---

## License

This project is built for educational purposes as part of an AI/ML internship assignment.

---

**Questions or Issues?** Check the inline code comments or review the prompt files for detailed explanations of how each component works.
