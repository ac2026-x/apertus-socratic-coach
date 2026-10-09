import os
from dotenv import load_dotenv
from openai import OpenAI

# Load hidden environment variables from .env
load_dotenv()

api_key = os.getenv("HF_API_KEY")

if not api_key:
    raise ValueError("API Key not found! Verify your .env file exists and contains HF_API_KEY.")

# Initialize OpenAI client for Hugging Face Router API
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=api_key
)

print("Sending request to Apertus model...")

try:
    response = client.chat.completions.create(
        model="swiss-ai/Apertus-v1.5-8B-Instruct",
        messages=[
            {"role": "system", "content": "You are a helpful science tutor."},
            {"role": "user", "content": "Why is the sky blue? Answer in one short sentence."}
        ],
        max_tokens=100,
        temperature=0.3
    )

    print("\n--- Apertus Response ---")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"\nAPI Request Failed: {e}")