# 🎂 WhatsApp Birthday AI Agent

A simple AI agent using **LangGraph ReAct** that checks if today is the user's birthday. The agent only accepts dates in **DD-MM-YYYY format** (day-month-year).

## 📋 Features

- ✅ **Strict Date Format**: Only accepts DD-MM-YYYY format
- 🎯 **Birthday Detection**: Compares user's birthday with today's date
- 💬 **WhatsApp-Friendly**: Conversational responses perfect for messaging
- 🔧 **LangGraph ReAct**: Uses advanced AI agent architecture
- 🛡️ **Error Handling**: Graceful handling of invalid inputs

## 🏗️ Project Structure

```
whatsapp-birthday-agent/
│
├── config.py              # Configuration settings
├── tools.py               # Birthday checking tool
├── prompts.py             # System prompts
├── agent.py               # Core agent functionality  
├── chat_interface.py      # Command-line interface
├── examples.py            # Usage examples and tests
├── main.py                # Main entry point
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project files
# Install dependencies
pip install -r requirements.txt
```

### 2. Setup API Key

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-openai-api-key-here"
```

### 3. Run the Agent

```bash
# Interactive chat mode
python main.py

# View examples
python main.py --examples

# Run tests
python main.py --test
```

## 💬 Usage Examples

### Valid Interactions:
```
User: "Hello!"
Agent: "Welcome! Please input your date of birth in DD-MM-YYYY format (day-month-year). Example: 25-12-1997"

User: "My birthday is 25-12-1997"
Agent: "Not your birthday today"

User: "04-09-2025"  # If today is Sep 4th
Agent: "Happy Birthday 🎉"
```

### Invalid Formats:
```
User: "Born on 12/25/1997"  # Wrong format
Agent: "Please provide date in DD-MM-YYYY format (day-month-year). Example: 25-12-1997"

User: "1997-12-25"  # Wrong format
Agent: "Please provide date in DD-MM-YYYY format (day-month-year). Example: 25-12-1997"
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Model settings
MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0.1

# Date format
DATE_FORMAT = "%d-%m-%Y"  # DD-MM-YYYY
DATE_EXAMPLE = "25-12-1997"

# Messages
WELCOME_MESSAGE = "Welcome! Please input your date of birth..."
BIRTHDAY_MESSAGE = "Happy Birthday 🎉"
```

## 🏗️ Architecture

The agent follows a clean, modular architecture:

1. **config.py**: Centralized configuration
2. **tools.py**: LangChain tool for birthday checking  
3. **prompts.py**: System prompts for the agent
4. **agent.py**: Core LangGraph ReAct agent setup
5. **chat_interface.py**: User interaction interface
6. **examples.py**: Testing and demonstration code
7. **main.py**: Entry point with CLI options

## 🛠️ Integration

### WhatsApp API Integration Example:

```python
from agent import create_birthday_agent

# Create agent instance
agent = create_birthday_agent()

def handle_whatsapp_message(phone_number: str, message: str) -> str:
    """Process WhatsApp message through birthday agent."""
    return agent.process_message(message)

# Use in your WhatsApp webhook
response = handle_whatsapp_message("+1234567890", "My birthday is 25-12-1997")
```

## 📝 Command Line Options

```bash
python main.py                 # Interactive chat mode
python main.py --examples      # Show usage examples
python main.py --test          # Run test scenarios  
python main.py --integration   # Show integration example
python main.py --help-detailed # Detailed help
```

## 🧪 Testing

Run the built-in test scenarios:

```bash
python main.py --test
```

Or run examples:

```bash
python main.py --examples
```

## 🔒 Requirements

- **Python**: 3.8+
- **LangChain**: Latest version
- **OpenAI API**: Valid API key
- **Dependencies**: See `requirements.txt`

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to fork, modify, and submit pull requests!

---

**Built with ❤️ using LangGraph ReAct**