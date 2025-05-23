from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from python_app.models import Base
# The following model imports are not strictly necessary here for db setup if Base is correctly populated
# but they don't hurt. They are needed if you were to directly use the models in this file.
from python_app.models.chat_memory_model import ChatMemoryModel
from python_app.models.pantry_model import PantryModel

# Import Blueprints
from python_app.routes.curl_routes import curl_bp
from python_app.routes.ollama_routes import ollama_bp

# LLM Imports
from langchain_community.chat_models.fake import FakeListChatModel
from python_app.agents.storage_agent import PythonStorageAgent
from python_app.llm_orchestrator import PythonLLMOrchestrator
from python_app.config import settings # Import settings

import logging # For logging configuration

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Ensure all models are imported so Base has them registered
    Base.metadata.create_all(bind=engine)

app = Flask(__name__)

# Configure basic logging if not already done for app startup messages
# (Flask's default logger might only activate on first request or if debug is True)
# We already set app.logger.setLevel(logging.INFO) later, so basicConfig might conflict or be redundant.
# Let's rely on Flask's logger and ensure its level is set.
# if not app.debug:
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Access settings and log them
# Ensuring app.logger is configured before use
if not app.logger.handlers: # Check if handlers are configured
    # If running standalone (not via flask run), handlers might not be set up yet.
    # For simplicity, we assume Flask's default setup or that app.logger.setLevel below is sufficient.
    pass

app.logger.info(f"Application Name: {settings.APP_NAME}")
app.logger.info(f"Attempting to load OpenAI API Key: {'present' if settings.OPENAI_API_KEY != 'dummy_openai_api_key' else 'not present (default will be used)'}") # Changed German to English
app.logger.info(f"Using OpenAI Model: {settings.OPENAI_MODEL_NAME}")
app.logger.info(f"Using OpenAI Temperature: {settings.OPENAI_TEMPERATURE}")


# Initialize LLM components
# You can add more varied responses to test different scenarios
fake_llm_responses = [
    "I am a fake LLM. You said: pantry stuff. My system prompt makes me confused.",
    "You asked about chat. I am still a fake LLM, and quite confused.",
    "Regarding your query: As a confused LLM, I can only offer generic advice."
]
# Initialize the chat model with a list of responses
chat_model = FakeListChatModel(responses=fake_llm_responses)
storage_agent = PythonStorageAgent(chat_model=chat_model)
llm_orchestrator_instance = PythonLLMOrchestrator(storage_agent=storage_agent)

# Make the orchestrator instance available to routes via app.config
app.config['LLM_ORCHESTRATOR'] = llm_orchestrator_instance

# Configure logging
app.logger.setLevel(logging.INFO) # Set default logging level for the app

# Register Blueprints
app.register_blueprint(curl_bp)
app.register_blueprint(ollama_bp)

@app.before_request
def before_request_hook():
    g.db_session = SessionLocal()
    app.logger.debug("DB Session created for request.")

@app.teardown_request
def teardown_request_hook(exception=None):
    db_session = g.pop('db_session', None)
    if db_session is not None:
        db_session.close()
        app.logger.debug("DB Session closed for request.")
    if exception:
        app.logger.error(f"Exception during request: {exception}")


@app.route('/')
def hello(): 
    return 'Hello, World!'

if __name__ == '__main__':
    init_db()
    app.logger.info("Database initialized.")
    app.run(debug=True)
