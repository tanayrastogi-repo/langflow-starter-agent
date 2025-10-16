# Langflow Marimo Chat

A small Marimo notebook that talks to a Langflow agent through its REST API.

## Requirements
- Python 3.13+
- Dependencies from `pyproject.toml` (install with `uv sync` or `pip install -r requirements.txt` if you export one)
- A running Langflow instance at `http://localhost:7860`
- Environment variables: `LANGFLOW_API_KEY`

## Run
```bash
export LANGFLOW_API_KEY=your-key
# Start the langflow server with the flow 
uv run langflow run "Simple Agent.json"
# Run the marimo as an app
uv marimo run notebook.py

