# langchain_helper.py  (Groq client version)
import os
from dotenv import load_dotenv
load_dotenv()

# Official Groq Python client
from groq import Groq
from prompts import EXPLAIN_PROMPT, TEST_PROMPT

# Create client (it will read API key from env if not provided explicitly)
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise RuntimeError("GROQ_API_KEY not set in .env — add your Groq API key to .env")

# instantiate client (you can also rely on env, but pass explicitly for clarity)
client = Groq(api_key=groq_api_key)

# choose a model — Llama 3.1 instant variants are commonly available on Groq
# pick "llama-3.1-8b-instant" or "llama-3.1-70b-instant" depending on your quota
DEFAULT_MODEL = "llama-3.1-8b-instant"

def _call_groq_chat(prompt_text: str, model: str = DEFAULT_MODEL, temperature: float = 0.0, max_tokens: int = 1500) -> str:
    """
    Calls Groq chat completions API and returns assistant text.
    """
    # Build messages array similar to OpenAI chat API
    messages = [
        {"role": "system", "content": "You are a senior expert Python developer."},
        {"role": "user", "content": prompt_text},
    ]

    # Call Groq chat completions
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # Extract text robustly — Groq responses are similar to other chat APIs
    try:
        # try attribute access
        content = resp.choices[0].message["content"]
    except Exception:
        try:
            data = resp.to_dict() if hasattr(resp, "to_dict") else dict(resp)
            content = data["choices"][0]["message"]["content"]
        except Exception:
            # as fallback, stringify response
            content = str(resp)

    return content

def explain_code(code: str, temperature: float = 0.0) -> str:
    prompt = EXPLAIN_PROMPT.format(code=code)
    return _call_groq_chat(prompt_text=prompt, temperature=temperature)

def generate_tests(code: str, temperature: float = 0.0) -> str:
    prompt = TEST_PROMPT.format(code=code)
    return _call_groq_chat(prompt_text=prompt, temperature=temperature)
