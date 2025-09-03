# examples.py
# Example usage and testing for WhatsApp Birthday AI Agent

from datetime import datetime
from agent import create_birthday_agent
from config import WELCOME_MESSAGE

def run_examples():
    """
    Example usage of the WhatsApp Birthday AI Agent.
    Shows how to integrate with actual WhatsApp API or messaging service.
    """
    print("🧪 WhatsApp Birthday AI Agent - Example Usage")
    print("=" * 60)
    
    # Create agent instance
    agent = create_birthday_agent()
    
    # Example messages in DD-MM-YYYY format
    test_messages = [
        "Hello!",
        "My birthday is 25-12-1990",
        f"I was born on {datetime.now().strftime('%d-%m-%Y')}",  # Today's date in DD-MM-YYYY
        "Born on 15-01-1995",
        "My DOB is 12/25/1990",  # Wrong format
        "25-13-1995",  # Invalid date (month 13)
        "Hi there, how are you?",
        "04-09-2025"  # September 4th format
    ]
    
    # Show welcome message first
    print(f"🤖 Agent: {WELCOME_MESSAGE}")
    print("-" * 60)
    
    # Process each test message
    for i, msg in enumerate(test_messages, 1):
        print(f"Test {i}:")
        print(f"User: {msg}")
        response = agent.process_message(msg)
        print(f"Agent: {response}")
        print("-" * 60)

def test_birthday_scenarios():
    """
    Test specific birthday scenarios.
    """
    print("\n🎯 Testing Birthday Scenarios")
    print("=" * 40)
    
    agent = create_birthday_agent()
    today = datetime.now()
    
    # Test cases
    test_cases = [
        {
            "name": "Today's Birthday",
            "date": today.strftime('%d-%m-%Y'),
            "expected": "Happy Birthday 🎉"
        },
        {
            "name": "Not Birthday",
            "date": "01-01-1990",
            "expected": "Not your birthday today"
        },
        {
            "name": "Wrong Format",
            "date": "1990-12-25",
            "expected": "Please provide date"
        },
        {
            "name": "Invalid Date",
            "date": "32-13-1990",
            "expected": "Invalid date"
        }
    ]
    
    for test in test_cases:
        print(f"\n{test['name']}:")
        print(f"Input: {test['date']}")
        response = agent.process_message(f"My birthday is {test['date']}")
        print(f"Response: {response}")
        
        # Check if response contains expected text
        if any(expected_word in response.lower() for expected_word in test['expected'].lower().split()):
            print("✅ Test Passed")
        else:
            print("❌ Test Failed")

def integration_example():
    """
    Example of how to integrate with WhatsApp API or other messaging services.
    """
    print("\n📱 Integration Example")
    print("=" * 30)
    
    # This is how you would integrate with WhatsApp API
    agent = create_birthday_agent()
    
    def handle_whatsapp_message(phone_number: str, message: str) -> str:
        """
        Handle incoming WhatsApp message.
        
        Args:
            phone_number (str): User's phone number
            message (str): User's message
            
        Returns:
            str: Response to send back
        """
        # Process message through birthday agent
        response = agent.process_message(message)
        
        # Log the interaction (in real app, use proper logging)
        print(f"User {phone_number}: {message}")
        print(f"Bot Response: {response}")
        
        return response
    
    # Example interactions
    example_interactions = [
        ("+1234567890", "Hello!"),
        ("+1234567890", "My birthday is 15-08-1995"),
        ("+9876543210", f"Born on {datetime.now().strftime('%d-%m-%Y')}"),
    ]
    
    print("WhatsApp Integration Example:")
    for phone, message in example_interactions:
        response = handle_whatsapp_message(phone, message)
        print(f"→ Sent to {phone}: {response}\n")

if __name__ == "__main__":
    # Run all examples
    run_examples()
    test_birthday_scenarios()
    integration_example()