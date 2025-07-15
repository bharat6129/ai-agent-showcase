# Weather Bot (Google ADK)

This agent demonstrates how to build a simple weather bot using Google's Agent Development Kit (ADK). It can fetch current weather conditions for a specified location by integrating with a weather API (e.g., OpenWeatherMap, WeatherAPI.com).

## 💡 How it Works

The bot is designed to:
1.  Understand natural language queries about weather.
2.  Extract location information from the user's input.
3.  Call an external tool (a weather API) to get real-time data.
4.  Respond with the current weather conditions.

## ⚙️ Setup and Run

1.  **Prerequisites**:
    * A Google Cloud Project with the necessary APIs enabled (e.g., Vertex AI API for LLM calls).
    * An API key for your chosen weather service (e.g., `OPENWEATHER_API_KEY`).

2.  **Navigate to the directory**:
    ```bash
    cd google-adk-agents/weather-bot
    ```

3.  **Create a virtual environment (recommended)**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set environment variables**:
    * `export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"` (if required by your ADK setup)
    * `export OPENWEATHER_API_KEY="YOUR_WEATHER_API_KEY"` (replace with your actual key)

6.  **Run the bot**:
    ```bash
    python main.py
    ```

## 📚 Code Structure

* `main.py`: The main application logic.
* `tools/`: (Optional) Directory for custom weather API integration tools.
* `agents/`: (Optional) Directory for agent definitions.

---
