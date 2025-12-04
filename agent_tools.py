from llama_index.core.tools import FunctionTool
import asyncio
import aiohttp

# Import your existing async functions
from tools.places_service import fetch_places
from tools.weather_service import fetch_weather
from tools.traffic_service import get_travel_time
from tools.flight_service import search_flights

# --- WRAPPERS ---
# The Agent needs to know EXACTLY what arguments to pass.

async def search_tool(query: str, location: str = "Tokyo"):
    """Useful for finding museums, parks, or points of interest. 
    Returns a list of place names and IDs."""
    async with aiohttp.ClientSession() as session:
        return await fetch_places(session, query, location)

async def weather_tool(lat: float, lon: float):
    """Useful for checking if it will rain at a specific coordinate. 
    Returns weather summary."""
    async with aiohttp.ClientSession() as session:
        return await fetch_weather(session, lat, lon)

async def flight_tool(origin: str, destination: str, travel_date: str):
    """
    Useful for finding flight prices and booking links.
    Returns the estimated price and a URL to book the ticket.
    Date format: DD/MM/YYYY
    """
    async with aiohttp.ClientSession() as session:
        return await search_flights(origin, destination, travel_date)

async def traffic_tool(lat1: float, lon1: float, lat2: float, lon2: float):
    """
    Calculates driving time between two points.
    Input: Latitude and Longitude for Start (1) and End (2).
    """
    # WE handle the formatting, so the Agent can't mess it up.
    # Mapbox needs: "long,lat"
    coord_a = f"{lon1},{lat1}"
    coord_b = f"{lon2},{lat2}"
    
    async with aiohttp.ClientSession() as session:
        return await get_travel_time(session, coord_a, coord_b)

# --- CREATE THE TOOLBOX ---
# This is what we hand to the Agent.
tools = [
    FunctionTool.from_defaults(
        async_fn=search_tool,
        name="Place_Search",
        description="Finds places and their coordinates."
    ),
    FunctionTool.from_defaults(
        async_fn=weather_tool,
        name="Weather_Check",
        description="Checks if it is raining at a location."
    ),
    FunctionTool.from_defaults(
        async_fn=traffic_tool,
        name="Traffic_Calculator",
        description="Calculates driving time. Needs lat1, lon1, lat2, lon2."
    ),
    FunctionTool.from_defaults(
        fn=flight_tool,
        name="Flight_Finder",
        description="Checks flight prices and booking links. Inputs: origin (e.g., DEL), destination (e.g., PAR), travel_date (DD/MM/YYYY)."
    )
]