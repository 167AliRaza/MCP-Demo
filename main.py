import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import json
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import uvicorn

# Initialize FastMCP
mcp = FastMCP("Weather-Forecast-MCP-Server")

def get_coordinates(city_name: str) -> Optional[Dict[str, float]]:
    """
    Get latitude and longitude for a given city name using Open-Meteo Geocoding API.
    
    Args:
        city_name: Name of the city
        
    Returns:
        Dictionary with 'latitude', 'longitude', and 'name' or None if not found
    """
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    
    try:
        response = requests.get(geocoding_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "latitude": result["latitude"],
                "longitude": result["longitude"],
                "name": result["name"],
                "country": result.get("country", ""),
                "admin1": result.get("admin1", "")
            }
        return None
    except Exception as e:
        raise Exception(f"Geocoding error: {str(e)}")


def fetch_current_weather(city_name: str) -> Dict[str, Any]:
    """
    Fetch current weather data for a given city.
    
    Args:
        city_name: Name of the city
        
    Returns:
        Dictionary containing current weather data
    """
    # Get coordinates
    location = get_coordinates(city_name)
    if not location:
        raise ValueError(f"City '{city_name}' not found")
    
    # Fetch current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "snowfall",
            "weather_code",
            "cloud_cover",
            "pressure_msl",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m"
        ],
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm"
    }
    
    try:
        response = requests.get(weather_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            "location": {
                "city": location["name"],
                "country": location["country"],
                "region": location["admin1"],
                "latitude": location["latitude"],
                "longitude": location["longitude"]
            },
            "current": data["current"],
            "units": data.get("current_units", {}),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise Exception(f"Weather API error: {str(e)}")


def fetch_historical_weather(
    city_name: str, 
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch historical weather data for a given city.
    
    Args:
        city_name: Name of the city
        start_date: Start date in YYYY-MM-DD format (default: 30 days ago)
        end_date: End date in YYYY-MM-DD format (default: yesterday)
        
    Returns:
        Dictionary containing historical weather data
    """
    # Get coordinates
    location = get_coordinates(city_name)
    if not location:
        raise ValueError(f"City '{city_name}' not found")
    
    # Set default dates if not provided
    if not end_date:
        end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    if not start_date:
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    # Fetch historical weather
    weather_url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "apparent_temperature_max",
            "apparent_temperature_min",
            "apparent_temperature_mean",
            "sunrise",
            "sunset",
            "precipitation_sum",
            "rain_sum",
            "snowfall_sum",
            "precipitation_hours",
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "wind_direction_10m_dominant",
            "shortwave_radiation_sum"
        ],
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm"
    }
    
    try:
        response = requests.get(weather_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            "location": {
                "city": location["name"],
                "country": location["country"],
                "region": location["admin1"],
                "latitude": location["latitude"],
                "longitude": location["longitude"]
            },
            "date_range": {
                "start": start_date,
                "end": end_date
            },
            "daily": data["daily"],
            "units": data.get("daily_units", {}),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise Exception(f"Historical weather API error: {str(e)}")

@mcp.tool()
def get_weather_data(
    city_name: str,
    query_type: str = "current",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """
    this tool is used to fetch weather data based on the city name and the query type.
    
    Args:
        city_name: Name of the city to fetch weather for
        query_type: Type of query - "current" or "historical" (default: "current")
        start_date: Start date for historical data in YYYY-MM-DD format (optional)
        end_date: End date for historical data in YYYY-MM-DD format (optional)
        
    Returns:
        JSON string containing weather data
        
    Example usage:
        # Get current weather
        result = get_weather_data("London")
        
        # Get historical weather for last 30 days
        result = get_weather_data("Paris", query_type="historical")
        
        # Get historical weather for specific date range
        result = get_weather_data("Tokyo", query_type="historical", 
                                 start_date="2024-10-01", end_date="2024-10-31")
    """
    try:
        if query_type.lower() == "current":
            data = fetch_current_weather(city_name)
        elif query_type.lower() == "historical":
            data = fetch_historical_weather(city_name, start_date, end_date)
        else:
            raise ValueError(f"Invalid query_type: {query_type}. Must be 'current' or 'historical'")
        
        return json.dumps(data, indent=2)
    
    except Exception as e:
        error_response = {
            "error": str(e),
            "city_name": city_name,
            "query_type": query_type
        }
        return json.dumps(error_response, indent=2)


# Weather code descriptions for reference
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}


def decode_weather_code(code: int) -> str:
    """Helper function to decode weather codes"""
    return WEATHER_CODES.get(code, f"Unknown ({code})")



# app = FastAPI(title="Weather Forecast MCP Server")

# # Mount MCP first
# app.mount("/mcp", mcp.sse_app())

# @app.get("/")
# async def root():
#     return {
#         "message": "Weather-Forecast-MCP-Server-API is running",
#         "endpoints": {
#             "/mcp": "MCP streaming endpoint",
#             "/docs": "Swagger UI for testing",
#         },
#     }




if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)