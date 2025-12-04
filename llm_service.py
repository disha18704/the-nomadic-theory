import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# We use the 'flash' model because it's fast and cheap for simple logic
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_itinerary(context_data):
    print("brain_tool: Thinking about the itinerary...")
    
    # 1. The Prompt (The Instructions)
    # We explicitly tell it to act as a travel planner and USE the data provided.
    prompt = f"""
    You are a smart travel agent. Create a short itinerary based ONLY on the data below.
    
    DATA CONTEXT:
    {json.dumps(context_data, indent=2)}
    
    INSTRUCTIONS:
    1. If 'is_raining' is true, explicitly mention that you selected indoor activities.
    2. Mention the travel time between the locations.
    3. Output the result as a clear, friendly paragraph.
    """

    # 2. Call Gemini
    response = model.generate_content(prompt)
    
    print("brain_tool: Itinerary generated!")
    return response.text