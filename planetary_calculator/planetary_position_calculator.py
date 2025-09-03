"""
Planetary position calculation tool for Vedic astrology.
Handles the integration between user input and the astrology calculation engine.
"""

from typing import List, Dict, Any
from location_resolver import LocationResolver
from vedic_calculator_engine import VedicCalculatorEngine

def calculate_planetary_positions(
    birth_year: str,
    birth_month: str, 
    birth_day: str,
    birth_hour: str,
    birth_minute: str,
    district: str,
    state: str,
    country: str,
    user_name: str = "User"
) -> Dict[str, Any]:
    """
    Calculate planetary positions for given birth details and location.
    
    This function serves as the main interface for planetary position calculations,
    coordinating between location resolution and astrological computations.
    
    Args:
        birth_year (str): Year of birth (e.g., "1990")
        birth_month (str): Month of birth (1-12)
        birth_day (str): Day of birth (1-31)
        birth_hour (str): Hour of birth in 24-hour format (0-23)
        birth_minute (str): Minute of birth (0-59)
        district (str): District/city of birth
        state (str): State/province of birth
        country (str): Country of birth
        user_name (str, optional): Name of the user. Defaults to "User"
        
    Returns:
        Dict[str, Any]: Dictionary containing:
            - success (bool): Whether calculation was successful
            - positions (List[str]): Formatted planetary positions
            - error (str, optional): Error message if calculation failed
            
    Example:
        >>> result = calculate_planetary_positions(
        ...     "1990", "5", "15", "14", "30",
        ...     "Mumbai", "Maharashtra", "India", "John"
        ... )
        >>> print(result['positions'])
        ['Sun      : 054° 23' → 24° 23' Taurus', ...]
    """
    try:
        # Validate and convert input parameters
        birth_data = _validate_birth_data(
            birth_year, birth_month, birth_day, birth_hour, birth_minute
        )
        
        # Resolve location to coordinates
        location_resolver = LocationResolver()
        coordinates = location_resolver.get_coordinates(district, state, country)
        
        if not coordinates:
            return {
                "success": False,
                "error": f"Could not resolve location: {district}, {state}, {country}"
            }
        
        latitude, longitude = coordinates
        
        # Calculate planetary positions
        calculator = VedicCalculatorEngine()
        planetary_positions = calculator.calculate_positions(
            name=user_name,
            year=birth_data['year'],
            month=birth_data['month'],
            day=birth_data['day'],
            hour=birth_data['hour'],
            minute=birth_data['minute'],
            latitude=latitude,
            longitude=longitude
        )
        
        return {
            "success": True,
            "positions": planetary_positions,
            "location": f"{district}, {state}, {country}",
            "coordinates": f"{latitude:.4f}°, {longitude:.4f}°"
        }
        
    except ValueError as e:
        return {
            "success": False,
            "error": f"Invalid birth data: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Calculation failed: {str(e)}"
        }

def _validate_birth_data(year: str, month: str, day: str, hour: str, minute: str) -> Dict[str, int]:
    """
    Validate and convert birth data strings to integers.
    
    Args:
        year, month, day, hour, minute (str): Birth data as strings
        
    Returns:
        Dict[str, int]: Validated birth data as integers
        
    Raises:
        ValueError: If any birth data is invalid
    """
    try:
        birth_data = {
            'year': int(year),
            'month': int(month),
            'day': int(day),
            'hour': int(hour),
            'minute': int(minute)
        }
        
        # Validate ranges
        if not (1900 <= birth_data['year'] <= 2100):
            raise ValueError(f"Year must be between 1900 and 2100, got {birth_data['year']}")
        
        if not (1 <= birth_data['month'] <= 12):
            raise ValueError(f"Month must be between 1 and 12, got {birth_data['month']}")
            
        if not (1 <= birth_data['day'] <= 31):
            raise ValueError(f"Day must be between 1 and 31, got {birth_data['day']}")
            
        if not (0 <= birth_data['hour'] <= 23):
            raise ValueError(f"Hour must be between 0 and 23, got {birth_data['hour']}")
            
        if not (0 <= birth_data['minute'] <= 59):
            raise ValueError(f"Minute must be between 0 and 59, got {birth_data['minute']}")
        
        return birth_data
        
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError("All birth data must be valid numbers")
        raise e