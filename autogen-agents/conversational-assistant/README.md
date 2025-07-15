# Conversational Assistant (AutoGen)

This example demonstrates a basic conversational assistant built using the AutoGen framework. It sets up two or more agents (e.g., a User Proxy Agent and an Assistant Agent) that can interact to answer questions or complete tasks.

## 💡 How it Works

The AutoGen conversational assistant typically involves:
* **User Proxy Agent**: Acts on behalf of the human user, sending prompts and receiving responses from other agents.
* **Assistant Agent**: An AI agent that processes requests, leverages tools (if configured), and responds.
* **Conversation Flow**: Agents exchange messages to collaboratively achieve a goal.

## ⚙️ Setup and Run

1.  **Prerequisites**:
    * An API key for an LLM provider (e.g., OpenAI, Azure OpenAI).

2.  **Navigate to the directory**:
    ```bash
    cd autogen-agents/conversational-assistant
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
    * `export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"` (replace with your actual key or other LLM provider keys)

6.  **Run the assistant**:
    ```bash
    python assistant.py
    ```

## 📚 Code Structure

* `assistant.py`: The main script defining the AutoGen agents and their conversation.

---
