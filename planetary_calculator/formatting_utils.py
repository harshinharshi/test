"""
Utility functions for formatting astrological data and positions.
Provides consistent formatting for planetary positions and calculations.
"""

from typing import List

class PositionFormatter:
    """Handles formatting of planetary positions into readable strings."""
    
    def __init__(self, zodiac_signs: List[str]):
        """
        Initialize formatter with zodiac signs.
        
        Args:
            zodiac_signs (List[str]): List of 12 zodiac signs in order
        """
        self.zodiac_signs = zodiac_signs
    
    def format_position(self, celestial_body_name: str, longitude_degrees: float) -> str:
        """
        Format a celestial body's position into a readable string.
        
        Args:
            celestial_body_name (str): Name of the planet/point (e.g., "Sun", "Moon")
            longitude_degrees (float): Longitude in degrees (0-360)
            
        Returns:
            str: Formatted position string
            
        Example:
            "Sun      : 054° 23' → 24° 23' Taurus"
        """
        # Determine which zodiac sign (each sign is 30 degrees)
        sign_index = int(longitude_degrees // 30)
        zodiac_sign = self.zodiac_signs[sign_index]
        
        # Calculate degrees within the sign (0-29)
        degrees_in_sign = longitude_degrees % 30
        degrees = int(degrees_in_sign)
        minutes = int((degrees_in_sign - degrees) * 60)
        
        # Format with consistent spacing for alignment
        return (
            f"{celestial_body_name:9}: "
            f"{longitude_degrees:05.0f}° {minutes:02d}' → "
            f"{degrees:02d}° {minutes:02d}' {zodiac_sign}"
        )
    
    def format_coordinates(self, latitude: float, longitude: float) -> str:
        """
        Format geographic coordinates for display.
        
        Args:
            latitude (float): Latitude in degrees
            longitude (float): Longitude in degrees
            
        Returns:
            str: Formatted coordinate string
        """
        lat_dir = "N" if latitude >= 0 else "S"
        lon_dir = "E" if longitude >= 0 else "W"
        
        return f"{abs(latitude):.4f}°{lat_dir}, {abs(longitude):.4f}°{lon_dir}"