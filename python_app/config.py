import os
from dotenv import load_dotenv

# Path to .env file (assuming .env is in the same directory as this config.py, i.e. python_app/.env)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

# Check if .env exists and load it
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    # If .env is not found at the specific path, load_dotenv() can search in standard locations.
    # For this project, we expect .env to be in the python_app directory.
    # If it's not there, environment variables should be set externally.
    # We can add a print statement or log here if .env is not found, for debugging.
    # print(f"Warning: .env file not found at {dotenv_path}. Relying on environment variables or defaults.")
    pass # load_dotenv() will try to find .env if not found at path, or do nothing if no .env found


class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "dummy_openai_api_key") # Default if not set
    OPENAI_MODEL_NAME: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.0"))
    # Add other configurations as needed
    APP_NAME: str = os.getenv("APP_NAME", "Python Stift Home App")

settings = Settings()
