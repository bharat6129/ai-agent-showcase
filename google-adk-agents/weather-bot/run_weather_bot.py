import os
from dotenv import load_dotenv
load_dotenv()

import sys
from agent import agent, get_default_session_service
from google.adk.runners import Runner
from google.genai import types

import warnings
warnings.filterwarnings("ignore", module="google")

# Set up session service and runner
session_service = get_default_session_service()
APP_NAME = "weather_bot_cli"
USER_ID = "cli_user"
SESSION_ID = "cli_session"

runner = Runner(
    agent=agent,
    app_name=APP_NAME,
    session_service=session_service
)

print("Welcome to the Weather Bot CLI! Type your question (or 'exit' to quit).\n")

async def ensure_session():
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

async def chat():
    while True:
        user_input = input("[You]: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        # Prepare message
        content = types.Content(role='user', parts=[types.Part(text=user_input)])
        final_response = None
        async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = event.content.parts[0].text
                elif event.actions and event.actions.escalate:
                    final_response = f"Agent escalated: {event.error_message or 'No specific message.'}"
                break
        print(f"[Bot]: {final_response}\n")

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(ensure_session())
        asyncio.run(chat())
    except KeyboardInterrupt:
        print("\nExiting Weather Bot CLI.")
        sys.exit(0)