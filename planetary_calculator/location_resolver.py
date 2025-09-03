"""
Location resolution service for converting place names to geographic coordinates.
Uses OpenStreetMap's Nominatim API for geocoding.
"""

import requests
import time
from typing import Optional, Tuple

class LocationResolver:
    """
    Resolves location names to geographic coordinates using Nominatim API.
    
    This service converts district/state/country information into latitude and
    longitude coordinates required for astrological calculations.
    """
    
    def __init__(self):
        """Initialize the location resolver with API configuration."""
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.headers = {
            'User-Agent': 'VedicAstrologyCalculator/2.0 (Educational Purpose)'
        }
        self.request_delay = 1.0  # Respectful delay between API requests
    
    def get_coordinates(
        self,
        district: str,
        state: str,
        country: str
    ) -> Optional[Tuple[float, float]]:
        """
        Resolve location name to coordinates.
        
        Args:
            district (str): District or city name
            state (str): State or province name  
            country (str): Country name
            
        Returns:
            Optional[Tuple[float, float]]: (latitude, longitude) if found, None if failed
        """
        # Try different search queries in order of specificity
        search_queries = [
            f"{district}, {state}, {country}",  # Most specific
            f"{district}, {country}",           # Skip state if needed
            f"{state}, {country}"               # Fallback to state level
        ]
        
        for query in search_queries:
            coordinates = self._query_nominatim(query)
            if coordinates:
                print(f"✅ Location resolved: {query} → {coordinates[0]:.4f}°, {coordinates[1]:.4f}°")
                return coordinates
        
        # If all automated attempts fail, try manual input
        print(f"❌ Could not resolve location: {district}, {state}, {country}")
        return self._get_manual_coordinates()
    
    def _query_nominatim(self, query: str) -> Optional[Tuple[float, float]]:
        """
        Query Nominatim API for coordinates.
        
        Args:
            query (str): Location search query
            
        Returns:
            Optional[Tuple[float, float]]: Coordinates if found
        """
        params = {
            'q': query,
            'format': 'json',
            'limit': 1,
            'addressdetails': 1
        }
        
        try:
            # Respectful delay to avoid overwhelming the API
            time.sleep(self.request_delay)
            
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data and len(data) > 0:
                result = data[0]
                latitude = float(result['lat'])
                longitude = float(result['lon'])
                
                # Validate coordinate ranges
                if self._validate_coordinates(latitude, longitude):
                    return latitude, longitude
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"⚠️ API request failed for '{query}': {e}")
            return None
        except (KeyError, ValueError, IndexError) as e:
            print(f"⚠️ Invalid response data for '{query}': {e}")
            return None
    
    def _validate_coordinates(self, latitude: float, longitude: float) -> bool:
        """
        Validate that coordinates are within valid ranges.
        
        Args:
            latitude (float): Latitude value
            longitude (float): Longitude value
            
        Returns:
            bool: True if coordinates are valid
        """
        return -90 <= latitude <= 90 and -180 <= longitude <= 180
    
    def _get_manual_coordinates(self) -> Optional[Tuple[float, float]]:
        """
        Fallback method to get coordinates manually from user input.
        
        Returns:
            Optional[Tuple[float, float]]: User-entered coordinates or None
        """
        print("\n📍 Please enter coordinates manually:")
        print("You can find coordinates using Google Maps or other mapping services.")
        
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                lat_input = input(f"Latitude (-90 to 90): ").strip()
                lon_input = input(f"Longitude (-180 to 180): ").strip()
                
                if not lat_input or not lon_input:
                    print("❌ Please enter both latitude and longitude.")
                    continue
                
                latitude = float(lat_input)
                longitude = float(lon_input)
                
                if self._validate_coordinates(latitude, longitude):
                    return latitude, longitude
                else:
                    print("❌ Coordinates out of valid range. Please try again.")
                    
            except ValueError:
                print("❌ Please enter valid decimal numbers.")
            
            if attempt < max_attempts - 1:
                print(f"Attempt {attempt + 2} of {max_attempts}:")
        
        print("❌ Failed to get valid coordinates. Calculation cannot proceed.")
        return None