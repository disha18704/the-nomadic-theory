import os
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY") 

async def fetch_weather(session, lat, lon):
    print(f"weather_tool: Checking forecast for Lat:{lat}, Lon:{lon}...")
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"

    async with session.get(url) as response:
        if response.status != 200:
            print(f"Weather Error: {response.status}")
            return None
        
        data = await response.json()

        # --- Logic: Is it going to rain tomorrow? ---
        # We just check the first few forecast points for "Rain"
        will_rain = False
        forecast_summary = "Clear"
        
        # Check next 24 hours (8 datapoints x 3 hours)
        for entry in data.get('list', [])[:8]:
            weather_main = entry['weather'][0]['main']
            if weather_main == "Rain":
                will_rain = True
                forecast_summary = "Rainy"
                break
        
        print(f"weather_tool: Forecast is {forecast_summary}.")
        
        return {
            "summary": forecast_summary,
            "will_rain": will_rain,
            "temp": data['list'][0]['main']['temp']
        }


async def test_weather():
    lat, lon = 35.676, 139.650
    async with aiohttp.ClientSession() as session:
        weather = await fetch_weather(session, lat, lon)
        print(weather)

if __name__ == "__main__":
    if not WEATHER_API_KEY:
        print("Set your OPENWEATHER_API_KEY first!")
    else:
        asyncio.run(test_weather())