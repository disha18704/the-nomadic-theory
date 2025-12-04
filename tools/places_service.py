import os
import aiohttp
import asyncio
import json
from dotenv import load_dotenv

# Load the API Key from a .env file (or just paste it below for testing)
load_dotenv()
API_KEY =os.getenv("GOOGLE_API_KEY") # OR paste string here: "AIzaSy..."

# --- Interview Concept: Session Management ---
# We pass the 'session' in as an argument. Creating a new session for 
# every single request is slow (TCP Handshake overhead). 
# Re-using one session is much faster (Connection Pooling).

async def fetch_places(session, query, location="Tokyo"):
    print(f"search_tool: Searching Google for '{query}' in {location}...")
    
    url = "https://places.googleapis.com/v1/places:searchText"
    
    # THE MONEY SAVER: Field Masking
    # We only ask for the ID, Name, and Formatted Address.
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.id,places.formattedAddress,places.location"
    }

    payload = {
        "textQuery": f"{query} in {location}"
    }

    async with session.post(url, headers=headers, json=payload) as response:
        if response.status != 200:
            print(f"Error: {response.status}")
            return []
        
        data = await response.json()
        places = data.get('places', [])
        
        print(f"search_tool: Found {len(places)} places.")
        return places

# --- Quick Test Loop ---
async def test_run():
    # We create the session ONCE here
    async with aiohttp.ClientSession() as session:
        results = await fetch_places(session, "Cheap Sushi", "Tokyo")
        
        # Pretty print the first result to see the JSON structure
        if results:
            print("\n--- Example Data ---")
            print(json.dumps(results[0], indent=2))

if __name__ == "__main__":
    # Check if key is present
    if not API_KEY:
        print("STOP! You forgot to set your API_KEY.")
    else:
        asyncio.run(test_run())