# agent.py
# Core agent functionality for WhatsApp Birthday AI Agent

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE
from tools import TOOLS
from prompts import SYSTEM_PROMPT

class WhatsAppBirthdayAgent:
    """
    WhatsApp Birthday AI Agent using LangGraph ReAct.
    Checks if today is the user's birthday based on DD-MM-YYYY format input.
    """
    
    def __init__(self):
        """Initialize the birthday agent with LLM and tools."""
        self.llm = None
        self.agent = None
        self._setup_agent()
    
    def _setup_agent(self):
        """
        Set up the LangGraph ReAct agent with ChatOpenAI model and tools.
        """
        # Initialize the language model
        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            api_key=OPENAI_API_KEY
        )
        
        # Create the ReAct agent with LangGraph
        self.agent = create_react_agent(
            model=self.llm,
            tools=TOOLS,
            prompt=SYSTEM_PROMPT,
        )
    
    def process_message(self, user_message: str) -> str:
        """
        Process user message through the agent and return response.
        
        Args:
            user_message (str): User's input message
            
        Returns:
            str: Agent's response
        """
        try:
            # Invoke the agent with the user's message
            response = self.agent.invoke({
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
    
    def get_agent(self):
        """
        Get the underlying agent instance.
        
        Returns:
            LangGraph ReAct Agent: The configured agent
        """
        return self.agent

def create_birthday_agent():
    """
    Factory function to create a WhatsApp Birthday Agent.
    
    Returns:
        WhatsAppBirthdayAgent: Configured birthday agent instance
    """
    return WhatsAppBirthdayAgent()