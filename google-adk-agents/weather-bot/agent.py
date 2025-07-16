import os
from typing import Optional, Dict, Any
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

# --- Model Constants ---
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
MODEL_GPT_4O = "openai/gpt-4.1"
MODEL_CLAUDE_SONNET = "anthropic/claude-sonnet-4-20250514"

# --- Mock Weather Tool (Stateful) ---
def get_weather_stateful(city: str, tool_context: ToolContext) -> dict:
    """Retrieves weather, converts temp unit based on session state."""
    city_normalized = city.lower().replace(" ", "")
    preferred_unit = tool_context.state.get("user_preference_temperature_unit", "Celsius")
    mock_weather_db = {
        "newyork": {"temp_c": 25, "condition": "sunny"},
        "london": {"temp_c": 15, "condition": "cloudy"},
        "tokyo": {"temp_c": 18, "condition": "light rain"},
    }
    if city_normalized in mock_weather_db:
        data = mock_weather_db[city_normalized]
        temp_c = data["temp_c"]
        condition = data["condition"]
        if preferred_unit == "Fahrenheit":
            temp_value = (temp_c * 9/5) + 32
            temp_unit = "°F"
        else:
            temp_value = temp_c
            temp_unit = "°C"
        report = f"The weather in {city.capitalize()} is {condition} with a temperature of {temp_value:.0f}{temp_unit}."
        tool_context.state["last_city_checked_stateful"] = city
        return {"status": "success", "report": report}
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}

# --- Greeting and Farewell Tools ---
def say_hello(name: Optional[str] = None) -> str:
    """Provides a simple greeting. If a name is provided, it will be used."""
    if name:
        return f"Hello, {name}!"
    return "Hello there!"

def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    return "Goodbye! Have a great day."

# --- Guardrail Callbacks ---
def block_keyword_guardrail(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    """Blocks LLM call if user message contains 'BLOCK'."""
    last_user_message_text = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == 'user' and content.parts:
                if content.parts[0].text:
                    last_user_message_text = content.parts[0].text
                    break
    if "BLOCK" in last_user_message_text.upper():
        callback_context.state["guardrail_block_keyword_triggered"] = True
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="I cannot process this request because it contains the blocked keyword 'BLOCK'.")],
            )
        )
    return None

def block_paris_tool_guardrail(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
    """Blocks weather tool if city is Paris."""
    if tool.name == "get_weather_stateful":
        city_argument = args.get("city", "")
        if city_argument and city_argument.lower() == "paris":
            tool_context.state["guardrail_tool_block_triggered"] = True
            return {
                "status": "error",
                "error_message": f"Policy restriction: Weather checks for '{city_argument.capitalize()}' are currently disabled by a tool guardrail."
            }
    return None

# --- Sub-Agents ---
greeting_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="greeting_agent",
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting using the 'say_hello' tool. Do nothing else.",
    description="Handles simple greetings and hellos using the 'say_hello' tool.",
    tools=[say_hello],
)

farewell_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="farewell_agent",
    instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message using the 'say_goodbye' tool. Do not perform any other actions.",
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
    tools=[say_goodbye],
)

# --- Root Agent (Team Orchestrator) ---
agent = Agent(
    name="weather_agent_team",
    model=MODEL_GEMINI_2_0_FLASH,
    description="Main agent: Provides weather (state-aware unit), delegates greetings/farewells, saves report to state, enforces guardrails.",
    instruction=(
        "You are the main Weather Agent. Your job is to provide weather using 'get_weather_stateful'. "
        "The tool will format the temperature based on user preference stored in state. "
        "Delegate simple greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
        "Handle only weather requests, greetings, and farewells."
    ),
    tools=[get_weather_stateful],
    sub_agents=[greeting_agent, farewell_agent],
    output_key="last_weather_report",
    before_model_callback=block_keyword_guardrail,
    before_tool_callback=block_paris_tool_guardrail,
)

# --- Session Service and Runner Example (for CLI or script use) ---
def get_default_session_service():
    return InMemorySessionService()

def get_default_runner():
    session_service = get_default_session_service()
    return Runner(
        agent=agent,
        app_name="weather_bot_app",
        session_service=session_service
    )

# --- Exported symbols ---
__all__ = [
    "get_weather_stateful",
    "say_hello",
    "say_goodbye",
    "greeting_agent",
    "farewell_agent",
    "agent",
    "get_default_session_service",
    "get_default_runner",
]