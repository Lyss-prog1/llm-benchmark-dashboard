"""
run_benchmark.py

Entry point of the LLM Benchmark Dashboard. Loads API credentials from .env,
sends the same fixed set of prompts to Mistral, Gemini, and Hugging Face via
the functions defined in providers.py, and writes the raw results (latency,
response text, errors) to a timestamped JSON file under results/.

This is the "test harness" of the project: it does not judge response
quality or track experiments yet (that comes with Weights & Biases in the
next step) : its only job here is to run every provider under the same
conditions and record what happened, reliably.
"""
import weave
import json
import os

from provider_metadata import PROVIDER_METADATA
from datetime import datetime, timezone
from dotenv import load_dotenv
from mistralai.client import Mistral
from google import genai
from huggingface_hub import InferenceClient
from providers import call_mistral, call_gemini, call_hf #functions defined in providers.py 
from prompts import PROMPTS

load_dotenv()

weave.init("macubuntu-admin-mac/llm-benchmark-dashboard")

mistral_client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
hf_client = InferenceClient(token=os.environ["HF_API_TOKEN"])

@weave.op
def run_single_call(call_fn, client, prompt_text: str, use_case: str) -> dict:
    result = call_fn(prompt_text, client)
    result["use_case"] = use_case
    meta = PROVIDER_METADATA[result["provider"]]
    result["confidentiality"] = meta["confidentiality"]
    result["confidentiality_note"] = meta["confidentiality_note"]
    return result


def run():
    results = []
    for prompt_entry in PROMPTS:
        prompt_text = prompt_entry["prompt"]
        use_case = prompt_entry["use_case"]
        print(f"[{use_case}] Prompt: {prompt_text[:60]}...")
        for call_fn, client in [
                (call_mistral, mistral_client),
                (call_gemini, gemini_client),
                (call_hf, hf_client),
        ]:
            result = run_single_call(call_fn, client, prompt_text, use_case)            
            print(f"  {result['provider']}: {result['latency_seconds']:.2f}s "
                  f"{'OK' if result['error'] is None else 'ERROR: ' + result['error']}")
            results.append(result)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_path = f"results/run_{timestamp}.json" #new file created for each execution of the benchmark
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved {len(results)} results to {output_path}")


if __name__ == "__main__":
    run()
