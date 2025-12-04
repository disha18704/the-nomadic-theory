import urllib.parse
import random
import asyncio

# --- MOCK FLIGHT TOOL (ASYNC VERSION) ---
async def search_flights(origin: str, destination: str, date: str):
    print(f"flight_tool: Searching flights from {origin} to {destination} on {date}...")
    
    # Simulate a tiny delay (like a real API)
    await asyncio.sleep(1)
    
    base_url = "https://www.easemytrip.com/flights.html"
    params = {
        "source": origin,
        "dest": destination,
        "date": date,
        "src": "YOUR_AFFILIATE_ID"
    }
    booking_link = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    # Mock Price
    estimated_price = random.randint(30000, 60000)
    
    result = {
        "airline": "Indigo (Simulated)",
        "price": estimated_price,
        "currency": "INR",
        "booking_link": booking_link,
        "status": "Available"
    }
    
    print(f"flight_tool: Found price {estimated_price}")
    return result