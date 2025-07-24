# Hiring Assistant Chatbot

This project implements an intelligent Hiring Assistant chatbot for "TalentScout," a fictional recruitment agency specializing in technology placements. The chatbot assists in the initial screening of candidates by gathering essential information and generating relevant technical questions based on the candidate's declared tech stack.

## Features

- **Streamlit UI**: Clean, intuitive interface with sidebar controls
- **Input Validation**: Comprehensive validation for all user inputs
- **Dynamic Question Generation**: Uses OpenAI GPT to generate tailored technical questions
- **Conversation Management**: Handles retry, restart, and exit commands
- **Progress Tracking**: Visual progress indicator and data display
- **Modular Architecture**: Clean separation of concerns across multiple files

## Project Structure

```
chatbot/
├── main.py                  # Main Streamlit application
├── config.py               # Configuration and constants
├── validators.py           # Input validation functions
├── session_manager.py      # Session state management
├── conversation_handler.py # Main conversation logic
├── ai_service.py          # OpenAI integration
├── utils.py               # Utility functions and UI helpers
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable template
├── README.md             # This file
├── pyproject.toml        # Project configuration
└── uv.lock              # uv lock file
```

## Installation

1. **Install dependencies using uv package manager**:
   ```bash
   uv pip install -r requirements.txt
   ```


## Usage

Run the Streamlit application:
```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

## How It Works

1. **Greeting**: The chatbot introduces itself and explains available commands
2. **Information Collection**: Validates and collects candidate details:
   - Full Name (letters and spaces only)
   - Email Address (valid email format)
   - Phone Number (exactly 10 digits)
   - Years of Experience (whole numbers 0-50)
   - Desired Position(s) (comma-separated list)
   - Current Location (any text)
   - Tech Stack (any text)
3. **Question Generation**: Creates technical questions based on tech stack
4. **Conversation Management**: Handles special commands and maintains state

## Commands

- `exit`, `quit`, `bye`, `end` - End the conversation
- `retry`, `try again` - Repeat the current question
- `restart`, `start over` - Start from the beginning

## File Descriptions

### `main.py`
Main Streamlit application entry point. Handles UI setup and user interaction flow.

### `config.py`
Contains configuration constants including:
- Question steps and validation mapping
- Command keywords
- Initial greeting message

### `validators.py`
Input validation functions for each data type:
- Name validation (letters/spaces only)
- Email format validation
- Phone number validation (10 digits)
- Experience validation (whole numbers)
- Position parsing (comma-separated)
- Location and tech stack validation

### `session_manager.py`
Session state management and utility functions:
- Session initialization
- Message handling
- Conversation state tracking
- Chat history display

### `conversation_handler.py`
Main conversation processing logic:
- User input processing
- Command handling (exit, retry, restart)
- Validation orchestration
- Question flow management

### `ai_service.py`
OpenAI integration for generating technical questions:
- API client setup
- Question generation based on tech stack
- Error handling for API failures

### `utils.py`
UI utility functions:
- Sidebar creation with progress tracking
- Help documentation display
- Data export functionality

## Technical Details

- **Language**: Python 3.13+
- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-3.5-turbo
- **Package Manager**: uv
- **Architecture**: Modular design with separation of concerns

## Data Privacy

- No candidate data is permanently stored
- All interactions are session-based
- API calls are made securely to OpenAI
- Follows data privacy best practices

## Development

To extend the chatbot:

1. **Add new validation**: Create function in `validators.py`
2. **Add new question step**: Update `STEPS` in `config.py`
3. **Modify conversation flow**: Update `conversation_handler.py`
4. **Add UI features**: Extend `utils.py`
5. **Change AI behavior**: Modify `ai_service.py`

## Future Enhancements

- Database integration for candidate storage
- Multi-language support
- Advanced question difficulty levels
- Interview scheduling integration
- Sentiment analysis
- Custom company branding

## License

MIT License


# 🎉 Ollama Integration Complete!

## ✅ What's Been Implemented

### 🚀 **Dual AI Provider Support**
- **OpenAI GPT-3.5-turbo**: Cloud-based AI (requires API key)
- **Llama 3.1 8B (Ollama)**: Local AI model (private & free)

### 🔧 **Key Features Added**

1. **AI Provider Selection**:
   - Dropdown in sidebar to switch between OpenAI and Ollama
   - Real-time status indicators (✅/❌)
   - Automatic availability detection

2. **Enhanced UI**:
   - AI provider status display
   - Setup instructions for Ollama
   - Progress tracking for conversation
   - Better organized sidebar

3. **Improved Question Generation**:
   - Better prompts for both AI providers
   - Error handling for both services
   - Fallback mechanisms

4. **Setup Automation**:
   - `setup_ollama.sh` script for easy installation
   - Comprehensive documentation
   - Troubleshooting guide

### 📁 **Updated File Structure**
```
chatbot/
├── main.py                  # Main app with AI provider display
├── config.py               # AI provider configuration
├── ai_service.py           # Dual AI integration (OpenAI + Ollama)
├── utils.py                # Enhanced sidebar with AI controls
├── session_manager.py      # Session state management
├── conversation_handler.py # Conversation processing
├── validators.py           # Input validation
├── setup_ollama.sh         # Automated Ollama setup
├── OLLAMA_GUIDE.md         # Comprehensive Ollama guide
├── requirements.txt        # Updated dependencies
└── .env.example           # Environment configuration
```

## 🎯 **How to Use**

### **Option 1: Quick Start with Ollama (Recommended)**
```bash
# 1. Install Ollama and Llama 3.1 8B
./setup_ollama.sh

# 2. Start the chatbot
streamlit run main.py

# 3. Select "Llama 3.1 8B (Ollama)" from the sidebar
```

### **Option 2: Use OpenAI**
```bash
# 1. Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"

# 2. Start the chatbot
streamlit run main.py

# 3. Select "OpenAI GPT-3.5-turbo" from the sidebar
```

## 🔍 **What Users Will See**

1. **Sidebar AI Configuration**:
   - ✅ Available AI providers
   - ❌ Unavailable providers with setup instructions
   - Current provider selection

2. **Main Chat Interface**:
   - Current AI provider display
   - All existing chatbot functionality
   - Enhanced help documentation

3. **Real-time Status**:
   - Ollama connection status
   - Model availability
   - Error messages with solutions

## 🛠 **Technical Benefits**

### **Privacy & Security**
- **Local Processing**: Ollama runs entirely on your machine
- **No Data Transmission**: Candidate data never leaves your system
- **Zero API Costs**: Free after initial setup

### **Performance**
- **Faster Responses**: No network latency with Ollama
- **Reliability**: No internet dependency
- **Customizable**: Can fine-tune models for specific needs

### **Flexibility**
- **Easy Switching**: Toggle between AI providers instantly
- **Fallback Options**: Multiple AI providers available
- **Extensible**: Easy to add more AI providers

## 📊 **Comparison**

| Feature | OpenAI GPT-3.5-turbo | Llama 3.1 8B (Ollama) |
|---------|----------------------|------------------------|
| **Privacy** | Cloud-based | 100% Local |
| **Cost** | Pay per use | Free after setup |
| **Speed** | Fast | Medium |
| **Quality** | Very High | High |
| **Setup** | API key only | Install + Download |
| **Internet** | Required | Not required |

## 🎓 **Next Steps**

1. **Try Both Providers**: Test the differences in question quality
2. **Customize Prompts**: Modify prompts in `ai_service.py`
3. **Add More Models**: Extend to support other Ollama models
4. **Fine-tune**: Train Llama on your specific interview data
5. **Deploy**: Set up production deployment with both providers

## 🔧 **Troubleshooting**

If you see "❌ Ollama not available":
1. Run `./setup_ollama.sh`
2. Ensure Ollama is running: `ollama serve`
3. Check the model is downloaded: `ollama list`

## 🚀 **Ready to Go!**

Your chatbot now supports both cloud-based and local AI processing, giving you the best of both worlds:
- **OpenAI**: For maximum quality and speed
- **Ollama**: For privacy, cost-effectiveness, and offline use

Switch between them anytime using the sidebar dropdown!
