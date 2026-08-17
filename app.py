import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key from .env
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Send a prompt to Gemini
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Introduce yourself as CampusAI, a helpful college assistant for students."
)

# Print the response
print(response.text)