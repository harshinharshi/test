# main.py
# Main entry point for WhatsApp Birthday AI Agent

"""
WhatsApp Birthday AI Agent using LangGraph ReAct

A simple AI agent that checks if today is the user's birthday.
Only accepts dates in DD-MM-YYYY format (day-month-year).

Usage:
    python main.py                  # Run interactive chat
    python main.py --examples       # Run examples
    python main.py --test          # Run tests

Author: AI Assistant
Version: 1.0
"""

import sys
import argparse
from chat_interface import main as run_chat
from examples import run_examples, test_birthday_scenarios, integration_example

def display_help():
    """Display help information about the application."""
    help_text = """
🎂 WhatsApp Birthday AI Agent - Help
=====================================

This AI agent checks if today is your birthday using LangGraph ReAct.

FEATURES:
- Only accepts DD-MM-YYYY format (day-month-year)
- Validates date format strictly
- Compares with today's date (month and day only)
- WhatsApp-friendly conversational responses

USAGE:
- python main.py              → Run interactive chat
- python main.py --examples   → Show usage examples  
- python main.py --test       → Run test scenarios
- python main.py --help       → Show this help

DATE FORMAT:
✅ Correct: 25-12-1997, 04-09-1990, 1-1-2000
❌ Wrong:   25/12/1997, 1997-12-25, Dec 25 1997

EXAMPLE INTERACTIONS:
User: "Hello!" → Agent: "Please input your date of birth in DD-MM-YYYY format..."
User: "My birthday is 25-12-1997" → Agent checks if today is Dec 25th
User: "04-09-2025" → Agent: "Happy Birthday 🎉" (if today is Sep 4th)

REQUIREMENTS:
- Python 3.8+
- langchain-openai
- langgraph  
- OpenAI API key

SETUP:
1. Install: pip install langchain-openai langgraph
2. Set API key: export OPENAI_API_KEY="your-key-here"
3. Run: python main.py
"""
    print(help_text)

def main():
    """
    Main entry point with command-line argument parsing.
    """
    parser = argparse.ArgumentParser(
        description="WhatsApp Birthday AI Agent using LangGraph ReAct",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--examples', 
        action='store_true', 
        help='Run example usage scenarios'
    )
    
    parser.add_argument(
        '--test', 
        action='store_true', 
        help='Run test scenarios'
    )
    
    parser.add_argument(
        '--integration', 
        action='store_true', 
        help='Show integration example'
    )
    
    parser.add_argument(
        '--help-detailed', 
        action='store_true', 
        help='Show detailed help information'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Handle different modes
        if args.help_detailed:
            display_help()
        
        elif args.examples:
            run_examples()
        
        elif args.test:
            test_birthday_scenarios()
        
        elif args.integration:
            integration_example()
        
        else:
            # Default: run interactive chat interface
            print("🚀 Starting WhatsApp Birthday AI Agent...")
            print("💡 Tip: Use --examples to see usage examples")
            print("💡 Tip: Use --help for more options\n")
            run_chat()
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\n📦 Please install required packages:")
        print("pip install langchain-openai langgraph")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()