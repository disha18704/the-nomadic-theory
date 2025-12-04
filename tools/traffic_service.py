import os
import aiohttp
import asyncio
import json
from dotenv import load_dotenv

load_dotenv()
MAPBOX_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")

async def get_travel_time(session, coord_a, coord_b):
    """
    Calculates driving time between two coordinates (Longitude, Latitude).
    Mapbox requires coordinates in format: "Long,Lat" (Google uses Lat,Long!)
    """
    print(f"traffic_tool: Calculating route...")

    # Construct the coordinate string "long1,lat1;long2,lat2"
    coordinates = f"{coord_a};{coord_b}"
    
    # We use the 'driving' profile
    url = f"https://api.mapbox.com/directions-matrix/v1/mapbox/driving/{coordinates}"
    
    params = {
        "access_token": MAPBOX_TOKEN,
        "annotations": "duration", # We only want time, not distance
    }

    async with session.get(url, params=params) as response:
        if response.status != 200:
            print(f"Mapbox Error: {response.status}")
            return None
        
        data = await response.json()
        
        # The result is a matrix. [0][1] is travel time from Point A to Point B.
        # duration is in seconds.
        duration_seconds = data['durations'][0][1]
        minutes = round(duration_seconds / 60)
        
        print(f"traffic_tool: Travel time is {minutes} mins.")
        return minutes

# --- Test Loop ---
async def test_traffic():
    # Example: Tokyo Tower -> Senso-ji Temple
    # Remember: Mapbox uses LONGITUDE first!
    tokyo_tower = "139.7454,35.6586"
    senso_ji = "139.7967,35.7148"
    
    async with aiohttp.ClientSession() as session:
        await get_travel_time(session, tokyo_tower, senso_ji)

if __name__ == "__main__":
    if not MAPBOX_TOKEN:
        print("Set your MAPBOX_ACCESS_TOKEN first!")
    else:
        asyncio.run(test_traffic())