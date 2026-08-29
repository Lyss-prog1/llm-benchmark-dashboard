"""
providers.py

Wraps each LLM provider's SDK behind a single, uniform function signature.
Each call_<provider>() function takes a prompt and a pre-built client, and
returns the same dict shape (provider, prompt, response, latency_seconds,
error) regardless of how that provider's SDK actually structures its
request/response : this is what lets run_benchmark.py treat all three
providers interchangeably in one loop instead of branching per provider.
"""
import weave
import time
from mistralai.client import Mistral
from google import genai
from huggingface_hub import InferenceClient

@weave.op
def call_mistral(prompt: str, client: Mistral) -> dict:
    start = time.perf_counter()
    try:
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        text = response.choices[0].message.content
        error = None
    except Exception as e:
        text = None
        error = str(e)
    latency = time.perf_counter() - start

    return {
        "provider": "mistral",
        "prompt": prompt,
        "response": text,
        "latency_seconds": latency,
        "error": error,
    }

@weave.op
def call_gemini(prompt: str, client: genai.Client) -> dict:
    start = time.perf_counter()
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        text = response.text
        error = None
    except Exception as e:
        text = None
        error = str(e)
    latency = time.perf_counter() - start

    return {
        "provider": "gemini",
        "prompt": prompt,
        "response": text,
        "latency_seconds": latency,
        "error": error,
    }

@weave.op
def call_hf(prompt: str, client: InferenceClient) -> dict:
    start = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        text = response.choices[0].message.content
        error = None
    except Exception as e:
        text = None
        error = str(e)
    latency = time.perf_counter() - start

    return {
        "provider": "huggingface",
        "prompt": prompt,
        "response": text,
        "latency_seconds": latency,
        "error": error,
    }
