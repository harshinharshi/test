# tools.py
# Tools for WhatsApp Birthday AI Agent

import re
from datetime import datetime
from langchain_core.tools import tool
from config import (
    DATE_FORMAT, 
    DATE_PATTERN, 
    FORMAT_ERROR_MESSAGE,
    BIRTHDAY_MESSAGE,
    NOT_BIRTHDAY_MESSAGE,
    INVALID_DATE_MESSAGE
)

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
        if not re.match(DATE_PATTERN, date_of_birth):
            return FORMAT_ERROR_MESSAGE
        
        # Parse the date in DD-MM-YYYY format
        dob_date = datetime.strptime(date_of_birth, DATE_FORMAT)
        
        # Get today's date
        today = datetime.now()
        
        # Compare month and day only
        if dob_date.month == today.month and dob_date.day == today.day:
            return BIRTHDAY_MESSAGE
        else:
            return NOT_BIRTHDAY_MESSAGE
            
    except ValueError as e:
        return INVALID_DATE_MESSAGE
    except Exception as e:
        return f"Error checking birthday: {str(e)}"

# List of all available tools
TOOLS = [check_birthday]