# chat_interface.py
# Chat interface for WhatsApp Birthday AI Agent

from agent import create_birthday_agent
from config import WELCOME_MESSAGE, DATE_EXAMPLE

class ChatInterface:
    """
    Command-line chat interface for the WhatsApp Birthday AI Agent.
    """
    
    def __init__(self):
        """Initialize the chat interface with the birthday agent."""
        self.agent = create_birthday_agent()
        self.running = False
    
    def display_startup_info(self):
        """Display startup information and welcome message."""
        print("🎂 WhatsApp Birthday AI Agent Started!")
        print("📝 This agent only accepts dates in DD-MM-YYYY format (day-month-year)")
        print(f"📅 Example: {DATE_EXAMPLE}")
        print("Type 'quit' to exit\n")
        
        # Show welcome message when agent starts
        print(f"🤖 Agent: {WELCOME_MESSAGE}\n")
    
    def get_user_input(self) -> str:
        """
        Get user input from command line.
        
        Returns:
            str: User's input message
        """
        return input("You: ").strip()
    
    def process_user_input(self, user_input: str) -> bool:
        """
        Process user input and return whether to continue.
        
        Args:
            user_input (str): User's input message
            
        Returns:
            bool: True to continue, False to exit
        """
        # Check for quit command
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            return False
        
        # Skip empty input
        if not user_input:
            return True
        
        # Process message through agent
        print("🤖 Agent: Processing...")
        response = self.agent.process_message(user_input)
        print(f"🤖 Agent: {response}\n")
        
        return True
    
    def run(self):
        """
        Run the main chat interface loop.
        """
        self.running = True
        self.display_startup_info()
        
        while self.running:
            try:
                user_input = self.get_user_input()
                self.running = self.process_user_input(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}\n")

def main():
    """
    Main function to run the WhatsApp Birthday AI Agent chat interface.
    """
    chat = ChatInterface()
    chat.run()

if __name__ == "__main__":
    main()