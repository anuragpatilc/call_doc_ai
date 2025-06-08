# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
MODEL_NAME = os.getenv("AZURE_OPENAI_MODEL_NAME")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
SUBSCRIPTION_KEY = os.getenv("AZURE_OPENAI_SUBSCRIPTION_KEY")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
