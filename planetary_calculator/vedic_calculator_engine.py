"""
Core Vedic Astrology calculation engine using Swiss Ephemeris.
Handles all astronomical calculations and astrological computations.
"""

import swisseph as swe
from datetime import datetime, timedelta
from typing import List, Tuple, Dict
from planetary_calculator.formatting_utils import PositionFormatter

class VedicCalculatorEngine:
    """
    Core engine for Vedic astrological calculations.
    
    This class handles all astronomical calculations using Swiss Ephemeris,
    configured for sidereal (Vedic) astrology with Lahiri ayanamsa.
    """
    
    # Planetary bodies to calculate
    PLANETS = {
        swe.SUN: "Sun",
        swe.MOON: "Moon",
        swe.MERCURY: "Mercury",
        swe.VENUS: "Venus", 
        swe.MARS: "Mars",
        swe.JUPITER: "Jupiter",
        swe.SATURN: "Saturn",
        swe.MEAN_NODE: "Rahu"  # North Node
    }
    
    # Zodiac signs in order
    ZODIAC_SIGNS = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    
    def __init__(self):
        """Initialize the Vedic calculator with proper ephemeris settings."""
        self._setup_ephemeris()
        self.formatter = PositionFormatter(self.ZODIAC_SIGNS)
    
    def _setup_ephemeris(self) -> None:
        """Configure Swiss Ephemeris for Vedic astrology calculations."""
        # Set ephemeris path (uses default if not specified)
        swe.set_ephe_path()
        
        # Set sidereal mode with Lahiri ayanamsa (standard for Vedic astrology)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    def calculate_positions(
        self,
        name: str,
        year: int,
        month: int, 
        day: int,
        hour: int,
        minute: int,
        latitude: float,
        longitude: float
    ) -> List[str]:
        """
        Calculate all planetary positions and ascendant for given birth details.
        
        Args:
            name (str): Name of the person (for reference)
            year (int): Birth year
            month (int): Birth month (1-12)
            day (int): Birth day (1-31)
            hour (int): Birth hour (0-23)
            minute (int): Birth minute (0-59)
            latitude (float): Birth location latitude
            longitude (float): Birth location longitude
            
        Returns:
            List[str]: Formatted list of planetary positions and ascendant
        """
        # Calculate Julian Day for the birth time
        julian_day = self._calculate_julian_day(year, month, day, hour, minute)
        
        # Calculate planetary positions
        planetary_results = self._calculate_planetary_positions(julian_day)
        
        # Calculate ascendant (rising sign)
        ascendant_result = self._calculate_ascendant(julian_day, latitude, longitude)
        
        # Combine all results
        all_results = planetary_results + [ascendant_result]
        
        return all_results
    
    def _calculate_julian_day(
        self,
        year: int,
        month: int,
        day: int, 
        hour: int,
        minute: int
    ) -> float:
        """
        Convert local birth time to Julian Day in UTC.
        
        Args:
            year, month, day, hour, minute: Birth date and time components
            
        Returns:
            float: Julian Day number in UTC
            
        Note:
            Currently assumes Indian Standard Time (UTC+5:30).
            For production use, implement proper timezone detection.
        """
        # Create local datetime
        local_datetime = datetime(year, month, day, hour, minute)
        
        # Convert to UTC (assuming IST UTC+5:30 for now)
        # TODO: Implement proper timezone detection based on coordinates
        utc_datetime = local_datetime - timedelta(hours=5, minutes=30)
        
        # Calculate Julian Day in UTC
        julian_day = swe.julday(
            utc_datetime.year,
            utc_datetime.month, 
            utc_datetime.day,
            utc_datetime.hour + utc_datetime.minute / 60.0
        )
        
        return julian_day
    
    def _calculate_planetary_positions(self, julian_day: float) -> List[str]:
        """
        Calculate positions for all planets including lunar nodes.
        
        Args:
            julian_day (float): Julian Day for calculations
            
        Returns:
            List[str]: Formatted planetary positions
        """
        results = []
        
        for planet_id, planet_name in self.PLANETS.items():
            if planet_name == "Rahu":
                # Handle Rahu-Ketu calculation (lunar nodes)
                rahu_ketu_results = self._calculate_lunar_nodes(julian_day, planet_id)
                results.extend(rahu_ketu_results)
            else:
                # Calculate regular planet position
                position_data = swe.calc(julian_day, planet_id, swe.FLG_SIDEREAL)
                longitude = position_data[0][0] % 360
                
                formatted_position = self.formatter.format_position(planet_name, longitude)
                results.append(formatted_position)
        
        return results
    
    def _calculate_lunar_nodes(self, julian_day: float, rahu_id: int) -> List[str]:
        """
        Calculate positions for Rahu (North Node) and Ketu (South Node).
        
        Args:
            julian_day (float): Julian Day for calculations
            rahu_id (int): Swiss Ephemeris ID for Rahu (Mean Node)
            
        Returns:
            List[str]: Formatted positions for Rahu and Ketu
        """
        # Calculate Rahu position
        rahu_data = swe.calc(julian_day, rahu_id, swe.FLG_SIDEREAL)
        rahu_longitude = rahu_data[0][0] % 360
        
        # Ketu is always exactly 180° opposite to Rahu
        ketu_longitude = (rahu_longitude + 180) % 360
        
        # Format both positions
        rahu_result = self.formatter.format_position("Rahu", rahu_longitude)
        ketu_result = self.formatter.format_position("Ketu", ketu_longitude)
        
        return [rahu_result, ketu_result]
    
    def _calculate_ascendant(
        self,
        julian_day: float,
        latitude: float,
        longitude: float
    ) -> str:
        """
        Calculate the Ascendant (Lagna) - the rising sign at birth.
        
        Args:
            julian_day (float): Julian Day for calculations
            latitude (float): Birth location latitude
            longitude (float): Birth location longitude
            
        Returns:
            str: Formatted Ascendant position
        """
        # Calculate house cusps and additional points
        house_cusps, ascmc = swe.houses_ex(
            julian_day,
            latitude,
            longitude,
            b'P',  # Placidus house system
            swe.FLG_SIDEREAL
        )
        
        # Ascendant is the first element in ascmc array
        ascendant_longitude = ascmc[0] % 360
        
        return self.formatter.format_position("Ascendant", ascendant_longitude)