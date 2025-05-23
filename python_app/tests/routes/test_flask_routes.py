import pytest
import json
from python_app.app import app, init_db # Import your Flask app instance and init_db

# The app instance from python_app.app should already have LLM_ORCHESTRATOR configured.
# We might need to ensure the DB is initialized for a test environment if routes interact with it,
# even if these specific tests don't directly show DB interaction.
# For these tests, the main concern is that app.config['LLM_ORCHESTRATOR'] is available.

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # If your app has a database setup function like init_db(), call it here
    # This ensures that if any route indirectly uses the DB (even via a hook not obvious here),
    # it's available. For an in-memory SQLite, this would be per-session or per-module.
    # However, our app.py currently uses a file-based SQLite "sqlite:///./app.db".
    # For tests, it's better to use a dedicated test DB or in-memory.
    # For now, we'll assume the existing app setup is sufficient, or that these routes
    # don't heavily depend on a pristine DB state for these specific checks.
    # A more robust setup would involve configuring a separate test database.
    # init_db() # This will use the "sqlite:///./app.db", which might persist state between test runs if not managed.
    # For now, let's proceed without explicit init_db in the client fixture,
    # as the app initializes it at startup if __name__ == '__main__', but not when imported.
    # The app.py also has `g.db_session` which uses `SessionLocal` tied to "sqlite:///./app.db".
    # This is a known issue for testing if tests run in parallel or if state is not cleaned.
    # Given the current app structure, these tests will run against the dev DB.

    with app.test_client() as client:
        yield client

def test_get_ollama_version(client):
    response = client.get('/ollama/api/version')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "version" in data
    assert data["version"] == "0.1.0_py_converted"

def test_post_curl_chat_valid(client):
    request_data = {"message": "Hello from test"}
    response = client.post('/curl/chat', json=request_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "reply" in data
    # The reply will come from FakeListChatModel via LLMOrchestrator
    # FakeListChatModel cycles through responses.
    # Check if it's one of the predefined fake responses or contains part of the input.
    # The current FakeListChatModel responses in app.py are:
    # - "I am a fake LLM. You said: pantry stuff. My system prompt makes me confused."
    # - "You asked about chat. I am still a fake LLM, and quite confused."
    # - "Regarding your query: As a confused LLM, I can only offer generic advice."
    # PythonStorageAgent prepends a system prompt, then user message.
    # The FakeListChatModel ignores the actual messages and just cycles through its list.
    # So, we expect one of these, not necessarily related to "Hello from test".
    fake_responses_from_app = [
        "I am a fake LLM. You said: pantry stuff. My system prompt makes me confused.",
        "You asked about chat. I am still a fake LLM, and quite confused.",
        "Regarding your query: As a confused LLM, I can only offer generic advice."
    ]
    assert data["reply"] in fake_responses_from_app

def test_post_curl_chat_invalid_missing_message(client):
    request_data = {"wrong_field": "test"}
    response = client.post('/curl/chat', json=request_data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert data["error"] == "Missing message"

def test_post_ollama_chat_valid(client):
    request_data = {"messages": [{"role": "user", "content": "Hello Ollama from test"}]}
    response = client.post('/ollama/api/chat', json=request_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["model"] == "workshop_py_converted"
    assert data["message"]["role"] == "assistant"
    # Similar to curl_chat, the content will be from FakeListChatModel's canned responses.
    fake_responses_from_app = [
        "I am a fake LLM. You said: pantry stuff. My system prompt makes me confused.",
        "You asked about chat. I am still a fake LLM, and quite confused.",
        "Regarding your query: As a confused LLM, I can only offer generic advice."
    ]
    assert data["message"]["content"] in fake_responses_from_app

def test_get_ollama_tags(client):
    response = client.get('/ollama/api/tags')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "models" in data
    assert len(data["models"]) > 0 # Mock returns one model
    assert data["models"][0]["name"] == "workshop_py:latest"
