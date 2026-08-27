from dotenv import load_dotenv
import os
from huggingface_hub import InferenceClient

load_dotenv()

api_token = os.environ["HF_API_TOKEN"]
client = InferenceClient(token=api_token)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "Reply with exactly one word: hello"}],
    temperature=0
)

print(response.choices[0].message.content)
