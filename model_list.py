import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
client = Groq()

# Fetch the active model list from Groq's servers
models_list = client.models.list()

print("Available Groq Model IDs for your API key:\n" + "="*40)
for model in models_list.data:
    print(f"- {model.id}")