# Weather Bot (Google ADK)

This agent demonstrates a robust, multi-agent weather bot using Google's Agent Development Kit (ADK). It features:

- **Mock weather data** (no external API required)
- **Multi-agent system**: root agent, greeting agent, farewell agent
- **Session state**: remembers user preferences (Celsius/Fahrenheit), last city checked
- **Delegation**: root agent delegates greetings/farewells to sub-agents
- **Guardrails**: blocks certain keywords and tool arguments (e.g., "BLOCK" or weather for Paris)
- **Interactive CLI**: chat with the bot in your terminal

## 💡 How it Works

- Understands natural language queries about weather, greetings, and farewells
- Maintains session state for personalized responses
- Delegates tasks to specialized sub-agents
- Enforces safety and policy guardrails

## ⚙️ Setup and Run

1. **Prerequisites**:
    * Python 3.8+
    * `google-adk` and `litellm` (see requirements.txt)

2. **Navigate to the directory**:
    ```bash
    cd google-adk-agents/weather-bot
    ```

3. **Create a virtual environment (recommended)**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the interactive CLI**:
    ```bash
    python run_weather_bot.py
    ```
    Type your questions (weather, greetings, farewells). Type `exit` or `quit` to leave.

6. **Run tests for mock weather logic**:
    ```bash
    python test_mock_weather.py
    ```

## 📚 Code Structure

* `agent.py`: All agent/team logic, tools, state, and guardrails
* `run_weather_bot.py`: Interactive CLI for chatting with the bot
* `test_mock_weather.py`: Tests for the mock weather tool
* `requirements.txt`: Python dependencies

## 🛡️ Guardrails
- Blocks user queries containing the word "BLOCK"
- Blocks weather requests for "Paris"

## 📝 Notes
- All weather data is mocked for demo/testing purposes
- Easily extendable to real APIs or more agents

---
