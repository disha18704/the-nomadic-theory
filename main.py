import asyncio
import aiohttp
import time
from dotenv import load_dotenv

# Import our "Senses" (The modules we built)
from tools.places_service import fetch_places
from tools.weather_service import fetch_weather
from tools.traffic_service import get_travel_time
from llm_service import generate_itinerary

# Load environment variables
load_dotenv()

async def main():
    print("--- 🚀 STARTING SMART ITINERARY PIPELINE ---")
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        # STEP 1: PARALLEL SEARCH (Extract)
        # We search for places AND check the general weather at the same time.
        # Note: We use Tokyo coordinates for weather default.
        print("\n[Phase 1] Gathering Data...")
        
        places_task = fetch_places(session, "Museums", "Tokyo")
        weather_task = fetch_weather(session, 35.676, 139.650) # Tokyo Lat/Lon
        
        # Run them together!
        places, weather = await asyncio.gather(places_task, weather_task)
        
        if not places:
            print("❌ No places found. Stopping.")
            return

        print(f"✅ Found {len(places)} places.")
        print(f"✅ Weather is: {weather['summary']} ({weather['temp']}°C)")

        # STEP 2: TRANSFORM (The "Smart" Filtering)
        # If it's raining, we should warn the user about outdoor places.
        # (For this prototype, we just print the status).
        
        print("\n[Phase 2] Analyzing Candidates...")
        
        # Let's take the first 2 places and check traffic between them
        place_a = places[0]
        place_b = places[1]
        
        # Extract coordinates from Google's response
        # Google returns: {'latitude': 35.6, 'longitude': 139.7}
        loc_a = place_a['location']
        loc_b = place_b['location']
        
        # Format for Mapbox (Long,Lat)
        coord_a = f"{loc_a['longitude']},{loc_a['latitude']}"
        coord_b = f"{loc_b['longitude']},{loc_b['latitude']}"
        
        # Calculate Traffic
        travel_minutes = await get_travel_time(session, coord_a, coord_b)
        
        # STEP 3: PREPARE FINAL DATA (Load)
        # This is the JSON object we WOULD send to Gemini.
        final_context = {
            "destination": "Tokyo",
            "weather_condition": weather['summary'],
            "is_raining": weather['will_rain'],
            "candidates": [
                {"name": place_a['displayName']['text'], "id": place_a['id']},
                {"name": place_b['displayName']['text'], "id": place_b['id']}
            ],
            "travel_time_between_top_2": f"{travel_minutes} mins"
        }

        print("\n[Phase 3] Generative AI Planning...")

        final_plan = generate_itinerary(final_context)

    total_time = time.time() - start_time
    
    print("\n" + "="*40)
    print(f"🏁 PIPELINE COMPLETE in {total_time:.2f} seconds")
    print("="*40)
    print("DATA READY FOR AI AGENT:")
    print(final_context)
    print(final_plan)

if __name__ == "__main__":
    asyncio.run(main())


    