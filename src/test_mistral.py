from dotenv import load_dotenv
import os
from mistralai.client import Mistral

load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

response = client.chat.complete(
    model="mistral-small-latest",
    messages=[{"role": "user", "content": "Reply with exactly one word: hello"}],
    temperature=0
)

print(response.choices[0].message.content)
