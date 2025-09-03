# config.py
# Configuration settings for WhatsApp Birthday AI Agent

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ===== API CONFIGURATION =====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ===== MODEL CONFIGURATION =====
MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0.1  # Low temperature for consistent responses

# ===== DATE FORMAT CONFIGURATION =====
DATE_FORMAT = "%d-%m-%Y"  # DD-MM-YYYY format
DATE_PATTERN = r'^\d{1,2}-\d{1,2}-\d{4}$'  # Regex pattern for DD-MM-YYYY
DATE_EXAMPLE = "25-12-1997"

# ===== MESSAGES CONFIGURATION =====
WELCOME_MESSAGE = "Welcome! Please input your date of birth in DD-MM-YYYY format (day-month-year). Example: 25-12-1997"
FORMAT_ERROR_MESSAGE = "Please provide date in DD-MM-YYYY format (day-month-year). Example: 25-12-1997"
BIRTHDAY_MESSAGE = "Happy Birthday 🎉"
NOT_BIRTHDAY_MESSAGE = "Not your birthday today"
INVALID_DATE_MESSAGE = "Invalid date. Please use DD-MM-YYYY format (day-month-year). Example: 25-12-1997"