import json
from typing import Any
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp  = FastMCP("weather")

async def query_weather(city: str) -> dict[str, Any] | None:
    return {
        "city": city,
        "weather": "sunny",
        "temperature": 60,
        "humidity": 50,
        "wind_speed": 10,
        "wind_direction": "N",
        "wind_gust": 20,
        "wind_gust_direction": "N",
        "wind_gust_speed": 30,
    }


@mcp.tool()
async def get_weather(city: str) -> str:
    data = await query_weather(city)
    wwather = f"The weather in {city} is {data['weather']} with a temperature of {data['temperature']} degrees Fahrenheit."
    return wwather

def main():
    # Initialize and run the server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()