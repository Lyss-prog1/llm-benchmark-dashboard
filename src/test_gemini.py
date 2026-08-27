from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

api_key = os.environ["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Reply with exactly one word: hello"
)

print(response.text)
