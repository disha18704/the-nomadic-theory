import os
import asyncio
from dotenv import load_dotenv
from llama_index.core.agent.workflow import ReActAgent
from llama_index.llms.google_genai import GoogleGenAI

# Import the toolbox
from agent_tools import tools

load_dotenv()

async def main():
    print("--- 🤖 INITIALIZING AI AGENT (WORKFLOW MODE) ---")
    
    # 1. Setup the Brain
    llm = GoogleGenAI(
        model_name="models/gemini-1.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    )

    # --- FIX 2: Initialize directly (No .from_tools) ---
    # The new version takes 'tools' and 'llm' directly in the constructor.
    # We add a timeout so it doesn't get stuck.
    agent = ReActAgent(
        tools=tools, 
        llm=llm, 
        verbose=True,
        timeout=120
    )

    # 3. Give it a Complex Task
    prompt = """
    I want to plan a trip to France. My budget is 50,000 INR.
    
    1. Search for a flight from Delhi (DEL) to Paris (CDG) for 25/12/2025.
    2. Check the flight price. If it is over my budget, stop and tell me.
    3. If within budget, find 2 museums in Paris and check the weather there.
    4. Finally, calculate the traffic time between the two museums.
    """
    
    print(f"\nUSER REQUEST: {prompt}\n")
    
    # --- FIX 3: Use .run() instead of .achat() ---
    # The new workflow agents use .run() to execute the workflow.
    response = await agent.run(user_msg=prompt)
    
    print("\n" + "="*40)
    print("FINAL RESPONSE:")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())