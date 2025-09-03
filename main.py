# WhatsApp Birthday AI Agent using LangGraph ReAct
# Simple agent that checks if it's the user's birthday - DD-MM-YYYY format only

import re
from datetime import datetime
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# ===== TOOLS =====
@tool
def check_birthday(date_of_birth: str) -> str:
    """
    Check if today matches the user's birthday (month and day).
    
    Args:
        date_of_birth (str): User's date of birth in DD-MM-YYYY format only
    
    Returns:
        str: Birthday message or not birthday message
    """
    try:
        # Only accept DD-MM-YYYY format (day-month-year)
        # Pattern: 1-2 digits, dash, 1-2 digits, dash, 4 digits
        if not re.match(r'^\d{1,2}-\d{1,2}-\d{4}$', date_of_birth):
            return "Please provide date in DD-MM-YYYY format (day-month-year). Example: 25-12-1997"
        
        # Parse the date in DD-MM-YYYY format
        dob_date = datetime.strptime(date_of_birth, '%d-%m-%Y')
        
        # Get today's date
        today = datetime.now()
        
        # Compare month and day only
        if dob_date.month == today.month and dob_date.day == today.day:
            return "Happy Birthday 🎉"
        else:
            return "Not your birthday today"
            
    except ValueError as e:
        return "Invalid date. Please use DD-MM-YYYY format (day-month-year). Example: 25-12-1997"
    except Exception as e:
        return f"Error checking birthday: {str(e)}"

# ===== SYSTEM PROMPT =====
SYSTEM_PROMPT = """
You are a WhatsApp Birthday AI Agent. Your main purpose is to check if today is the user's birthday.

IMPORTANT RULES:
1. You MUST ONLY respond if the user provides their date of birth (DOB)
2. If no DOB is provided, respond EXACTLY with: "Please input your date of birth in DD-MM-YYYY format (day-month-year). Example: 25-12-1997"
3. When DOB is provided, use the check_birthday tool to verify if it's their birthday
4. Accept ONLY DD-MM-YYYY format (day-month-year)
5. Be friendly and conversational like a WhatsApp chat

BEHAVIOR:
- Look for dates in DD-MM-YYYY format only (e.g., 25-12-1997, 05-07-1990)
- If you find a date in correct format, use check_birthday tool
- If date is in wrong format or no date found, ask for correct format
- Keep responses short and WhatsApp-friendly
- Use the check_birthday tool when you have a valid DD-MM-YYYY date

Examples:
User: "Hi there!" → Response: "Please input your date of birth in DD-MM-YYYY format (day-month-year). Example: 25-12-1997"
User: "My birthday is 25-12-1990" → Use tool and respond with result
User: "I was born on 05-07-1985" → Use tool and respond with result
User: "Born on 12/25/1985" → Response: "Please provide date in DD-MM-YYYY format (day-month-year). Example: 25-12-1997"
"""

# ===== TOOLS LIST =====
TOOLS = [check_birthday]

# ===== AGENT SETUP =====
def create_birthday_agent():
    """
    Create and return the WhatsApp Birthday AI Agent using LangGraph ReAct.
    
    Returns:
        LangGraph ReAct Agent: Configured agent ready to process messages
    """
    # Initialize the language model (tool functions reference this)
    # Note: In production, set the API key via environment variable
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.1,  # Low temperature for consistent responses
        api_key=OPENAI_API_KEY
    )
    
    # Create the ReAct agent with LangGraph
    llm_agent_graph = create_react_agent(
        model=llm,  # Pass the actual model instance
        tools=TOOLS,
        prompt=SYSTEM_PROMPT,
    )
    
    return llm_agent_graph

# ===== CHAT INTERFACE =====
def chat_with_agent(agent, user_message: str) -> str:
    """
    Process user message through the agent and return response.
    
    Args:
        agent: The LangGraph ReAct agent
        user_message (str): User's input message
        
    Returns:
        str: Agent's response
    """
    try:
        # Invoke the agent with the user's message
        response = agent.invoke({
            "messages": [("user", user_message)]
        })
        
        # Extract the agent's response from the messages
        agent_messages = response["messages"]
        
        # Get the last message from the agent (should be the response)
        for message in reversed(agent_messages):
            if hasattr(message, 'content') and message.content.strip():
                return message.content.strip()
        
        return "Sorry, I couldn't process that message."
        
    except Exception as e:
        return f"Error: {str(e)}"

# ===== MAIN EXECUTION =====
def main():
    """
    Main function to run the WhatsApp Birthday AI Agent.
    Provides a simple chat interface for testing.
    """
    print("🎂 WhatsApp Birthday AI Agent Started!")
    print("📝 This agent only accepts dates in DD-MM-YYYY format (day-month-year)")
    print("📅 Example: 25-12-1997")
    print("Type 'quit' to exit\n")
    
    # Create the agent
    agent = create_birthday_agent()
    
    # Show welcome message when agent starts
    print("🤖 Agent: Welcome! Please input your date of birth in DD-MM-YYYY format (day-month-year). Example: 25-12-1997\n")
    
    # Chat loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for quit command
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Process message through agent
            print("🤖 Agent: Processing...")
            response = chat_with_agent(agent, user_input)
            print(f"🤖 Agent: {response}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")

# ===== EXAMPLE USAGE =====
def example_usage():
    """
    Example usage of the WhatsApp Birthday AI Agent.
    Shows how to integrate with actual WhatsApp API or messaging service.
    """
    agent = create_birthday_agent()
    
    # Example messages in DD-MM-YYYY format
    test_messages = [
        "Hello!",
        "My birthday is 25-12-1990",
        f"I was born on {datetime.now().strftime('%d-%m-%Y')}",  # Today's date in DD-MM-YYYY
        "Born on 15-01-1995",
        "My DOB is 12/25/1990",  # Wrong format
        "25-13-1995"  # Invalid date (month 13)
    ]
    
    print("🧪 Example Usage:")
    print("=" * 50)
    
    # Show welcome message first
    print("🤖 Agent: Welcome! Please input your date of birth in DD-MM-YYYY format (day-month-year). Example: 25-12-1997")
    print("-" * 50)
    
    for msg in test_messages:
        print(f"User: {msg}")
        response = chat_with_agent(agent, msg)
        print(f"Agent: {response}")
        print("-" * 50)

if __name__ == "__main__":
    # Run the main chat interface
    # Uncomment the line below to run example usage instead
    # example_usage()
    main()