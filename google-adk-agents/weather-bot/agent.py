import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import os
import requests
from dotenv import load_dotenv
from dateutil import parser as date_parser
from datetime import datetime, timedelta
load_dotenv()

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


def get_live_weather(city: str) -> dict:
    """Fetches live weather data for a specified city using OpenWeatherMap API."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "error_message": "OpenWeatherMap API key not found in environment variable OPENWEATHER_API_KEY."
        }
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {
                "status": "error",
                "error_message": f"Failed to fetch weather data: {response.text}"
            }
        data = response.json()
        weather = data["weather"][0]["description"].capitalize()
        temp_c = data["main"]["temp"]
        temp_f = temp_c * 9/5 + 32
        report = (
            f"The weather in {city} is {weather} with a temperature of {temp_c:.1f}°C ({temp_f:.1f}°F)."
        )
        return {"status": "success", "report": report}
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Exception occurred: {e}"
        }


def get_weather_forecast(city: str, day: str = "tomorrow", units: str = "imperial") -> dict:
    """Fetches weather forecast for a specified city and day using OpenWeatherMap API. Day can be 'today', 'tomorrow', or a date string (YYYY-MM-DD). Units: 'imperial' (F), 'metric' (C)."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "error_message": "OpenWeatherMap API key not found in environment variable OPENWEATHER_API_KEY."
        }
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return {
                "status": "error",
                "error_message": f"Failed to fetch forecast data: {response.text}"
            }
        data = response.json()
        # Determine target date
        now = datetime.now()
        if day.lower() == "today":
            target_date = now.date()
        elif day.lower() == "tomorrow":
            target_date = (now + timedelta(days=1)).date()
        else:
            try:
                target_date = date_parser.parse(day).date()
            except Exception:
                return {"status": "error", "error_message": f"Could not parse day: {day}"}
        # Find forecast closest to noon on target date
        forecasts = data.get("list", [])
        target_forecast = None
        min_time_diff = timedelta(days=2)
        for entry in forecasts:
            dt_txt = entry.get("dt_txt")
            if not dt_txt:
                continue
            entry_dt = date_parser.parse(dt_txt)
            if entry_dt.date() == target_date:
                time_diff = abs(entry_dt.hour - 12)
                if time_diff < min_time_diff.total_seconds():
                    min_time_diff = timedelta(hours=time_diff)
                    target_forecast = entry
        if not target_forecast:
            return {"status": "error", "error_message": f"No forecast available for {city} on {target_date}."}
        weather = target_forecast["weather"][0]["description"].capitalize()
        temp = target_forecast["main"]["temp"]
        unit_symbol = "°F" if units == "imperial" else "°C"
        report = (
            f"The forecasted weather in {city} on {target_date} is {weather} with a temperature of {temp:.1f}{unit_symbol}."
        )
        return {"status": "success", "report": report}
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Exception occurred: {e}"
        }


root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time, live weather, and weather predictions in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time, live weather, and weather predictions (forecasts) in any city using real-time data. Use Fahrenheit if the user requests it."
    ),
    tools=[get_live_weather, get_current_time, get_weather_forecast],
)