import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Helpful warnings for common misconfiguration during development
if not DATABASE_URL:
    print("Warning: DATABASE_URL is not set. Create a .env file from .env.example and set DATABASE_URL.")

if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY is not set. LLM generation will fail without a valid key.")


