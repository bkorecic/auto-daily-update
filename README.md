# Auto daily update

Simple script to generate a daily update using an LLM

## Requirements

- (https://github.com/simonw/llm)[simonw/llm]: Install with `brew install llm`

## How to use

1. Configure your favorite model in llm by following the (https://llm.datasette.io/en/stable/usage.html)[instructions].
    - **Example with `gemini-2.0-flash`:**
    - Install the required plugin: `llm install llm-gemini`
    - Add the API key: `llm keys set gemini`
    - Set the default model: `llm models default gemini-2.0-flash`
    - Run a test prompt to check if it's working: `llm hi`
2. Edit `auto-daily-update.py` and
    - Set `FRONTEND_PATH` and `BACKEND_PATH` to the corresponding directories.
    - Set `AUTHOR` to your git name and email (find it in `git log`).
3. Run `auto-daily-update.py` whenever you want a summary of all commits in

