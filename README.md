# Code Explainer & Test Generator
A local Streamlit app that explains code, suggests refactors, and generates unit test stubs using an LLM (via LangChain/OpenAI).

## What's included
- `app.py` : Streamlit frontend
- `langchain_helper.py` : LLM prompt + invocation helpers
- `prompts.py` : Prompt templates for explanations and tests
- `requirements.txt` : Python dependencies
- `.env.example` : Example env file for API key
- `README.md` : This file

## Quick start (Windows / macOS / Linux)
1. Clone or unzip the project and open in VS Code.
2. Create a virtual environment:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv venv` then `source venv/bin/activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Create a `.env` file in the project root with:
   ```
   OPENAI_API_KEY=sk-...
   ```
5. Run the app:
   `streamlit run app.py`
6. In the UI: paste code or upload a `.py` file, pick an action and get results.

## Notes
- This project uses OpenAI via LangChain. You can replace the LLM with another provider supported by LangChain.
- The generated unit tests are suggestions; review before using them in production.
