# Auto daily update

Simple script to generate a daily update using an LLM

## Requirements

- [simonw/llm](https://github.com/simonw/llm): Install with `brew install llm`
- Python 3

## How to use

1. Configure your favorite model in llm by following the [instructions](https://llm.datasette.io/en/stable/usage.html).
    - **Example with `gemini-2.0-flash`:**
    - Install the required plugin: `llm install llm-gemini`
    - Add the API key: `llm keys set gemini`
    - Set the default model: `llm models default gemini-2.0-flash`
    - Run a test prompt to check if it's working: `llm hi`
2. Edit `auto-daily-update.py` and
    - Set `FRONTEND_PATH` and `BACKEND_PATH` to the corresponding directories.
    - Set `AUTHOR` to your configured name in `git`.
        - For example, if in `git log` your name appears as `Author: Blaz Korecic <blaz@niuro.io>`, `AUTHOR="Blaz"`, `AUTHOR="Blaz Korecic"` and `AUTHOR="Korecic"` will work.
3. Run `auto-daily-update.py` whenever you want a summary of all commits made by you this day in all branches.

## Warning

The result will be as good as your commit messages are.

## TODO

Improve the example
