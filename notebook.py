# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "requests==2.32.5",
# ]
# ///

import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells
    import marimo as mo
    import requests
    import os
    import uuid
    import json


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    # Agentic AI using Langflow
    A simple starter AI agent created using Langflow API. The flow is created using Langflow visual IDE that has access to Google Gemini model (gemini-flash-lite-latest). 

    The Langflow agent has access to following tools:
    * fetch_content: To fetch content from one or more web pages, following links recursively.
    * search_news: To search Google News via RSS and return clean article data.
    * evaluate_expression: To perform basic arithmetic operations on a given expression (a calculator).
    * get_current_date: To return the current date and time in a selected timezone.

    ----
    """
    )
    return


@app.cell
def _():
    ## Langflow API with Python
    # Reference: https://docs.langflow.org/get-started-quickstart
    def ask_agent(
        question: str,
        session_id: str,
        url: str = "http://localhost:7860/api/v1/run/ad69a481-6d94-4e43-b8b6-fdc5ff0b8f44",
    ):
        """
        Send a chat-style query to the Langflow REST endpoint.

        Builds a payload with the provided question and session identifier,
        submits it to the configured `url`, and returns the parsed JSON
        response from Langflow. If the request fails or raises an HTTP error,
        returns a string describing the failure.
        """
        # Request payload configuration
        payload = {
            "output_type": "chat",
            "input_type": "chat",
            "input_value": question,
            "tweaks": {
                "ChatInput-agoWZ": {"session_id": session_id},
            },
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": os.getenv("LANGFLOW_API_KEY"),
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            return f"Error: {str(e)}"


    def extract_message(data: json):
        """Unpack the assistant’s text reply from a Langflow JSON response."""
        try:
            return data["outputs"][0]["outputs"][0]["outputs"]["message"][
                "message"
            ]
        except (KeyError, IndexError):
            return None
    return ask_agent, extract_message


@app.cell
def _():
    # Get session id
    session_id = str(uuid.uuid4())
    mo.md(f"Session ID: {session_id}")
    return (session_id,)


@app.cell
def _(ask_agent, extract_message, session_id):
    def chat_model(messages, config):
        if not messages:
            return "Hi! Ask me anything about the agent."
        latest = messages[-1]
        if latest.role != "user":
            return None

        response = ask_agent(
            question=latest.content,
            session_id=session_id,
        )
        ai_answer = extract_message(response)
        return f"AI:{ai_answer}"


    chat = mo.ui.chat(chat_model)
    chat
    return


if __name__ == "__main__":
    app.run()
