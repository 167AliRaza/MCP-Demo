# Weather Forecast MCP Server

A Model Context Protocol (MCP) server that provides current and historical weather data for any city worldwide using the Open-Meteo API.

## Features

- 🌤️ Current weather data with 13+ parameters
- 📊 Historical weather data (up to years of history)
- 🌍 Global coverage for any city
- 🔄 MCP http with SSE Async endpoint
- ⚡ Fast and reliable (powered by Open-Meteo)

## Quick Start

### Using the Public Server

**Server URL:** `https://weather-mcp.fastmcp.app/mcp`

### Integration with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "weather": {
      "url": "https://weather-mcp.fastmcp.app/mcp"
    }
  }
}
```

### Integration with Other MCP Clients

```python
from mcp import ClientSession

async with ClientSession("https://weather-mcp.fastmcp.app/mcp") as session:
    result = await session.call_tool(
        "get_weather_data",
        city_name="London",
        query_type="current"
    )
    print(result)
```


## Tool Documentation

### `get_weather_data`

Fetch weather data for any city.

**Parameters:**
- `city_name` (string, required): Name of the city
- `query_type` (string, optional): "current" or "historical" (default: "current")
- `start_date` (string, optional): Start date for historical data (YYYY-MM-DD)
- `end_date` (string, optional): End date for historical data (YYYY-MM-DD)

**Returns:** JSON string with weather data

**Example Response (Current Weather):**
```json
{
  "location": {
    "city": "London",
    "country": "United Kingdom",
    "latitude": 51.5074,
    "longitude": -0.1278
  },
  "current": {
    "temperature_2m": 15.2,
    "relative_humidity_2m": 72,
    "wind_speed_10m": 12.5,
    "weather_code": 2
  }
}
```

## Self-Hosting

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/weather-mcp-server
cd weather-mcp-server

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

Server will start at `http://localhost:8000`

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000
CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t weather-mcp .
docker run -p 8000:8000 weather-mcp
```

## Weather Parameters

### Current Weather
- Temperature (°C)
- Apparent temperature (°C)
- Relative humidity (%)
- Precipitation (mm)
- Rain & Snowfall (mm)
- Weather code
- Cloud cover (%)
- Pressure (hPa)
- Wind speed, direction, gusts (km/h, °)

### Historical Weather
- Daily min/max/mean temperatures
- Apparent temperatures
- Sunrise/sunset times
- Precipitation totals
- Wind data
- Solar radiation

## Weather Codes

| Code | Description |
|------|-------------|
| 0 | Clear sky |
| 1-3 | Mainly clear to overcast |
| 45, 48 | Fog |
| 51-57 | Drizzle |
| 61-67 | Rain |
| 71-77 | Snow |
| 80-82 | Rain showers |
| 85-86 | Snow showers |
| 95-99 | Thunderstorm |

## Rate Limits

- Open-Meteo API: 10,000 requests/day (free tier)
- No authentication required

## Contributing

Contributions welcome! Please open an issue or PR.

## License

MIT License - feel free to use in your projects!

## Credits

- Weather data provided by [Open-Meteo](https://open-meteo.com/)
- Built with [FastMCP](https://github.com/jlowin/fastmcp)

## Support

- 📧 Email: 167aliraza@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/weather-mcp-server/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/weather-mcp-server/discussions)
