import pytest
import uuid
import json # Added import for json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from python_app.models import Base # Assuming Base is in python_app/models/__init__.py
from python_app.models.chat_memory_model import ChatMemoryModel
from python_app.services.chat_memory_store import PythonChatMemoryStore

@pytest.fixture(scope="function") # New DB and session for each test function
def db_session():
    # Using in-memory SQLite for tests
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine) # Create tables based on Base
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine) # Clean up tables

@pytest.fixture
def chat_memory_store(db_session: Session):
    return PythonChatMemoryStore(session=db_session)

def test_update_messages_new_id(chat_memory_store: PythonChatMemoryStore, db_session: Session):
    memory_id = "test_mem_1"
    messages_data = [{"role": "user", "content": "Hello"}]
    chat_memory_store.update_messages(memory_id, messages_data)
    
    # Verify directly in DB
    entry = db_session.query(ChatMemoryModel).filter_by(memory_id=memory_id).first()
    assert entry is not None
    assert entry.memory_id == memory_id
    assert json.loads(entry.json_messages) == messages_data

def test_get_messages_existing_id(chat_memory_store: PythonChatMemoryStore, db_session: Session):
    memory_id = "test_mem_2"
    messages_data = [{"role": "ai", "content": "Hi there"}]
    
    # Pre-populate
    # Ensure id is a UUID object for the model
    db_entry = ChatMemoryModel(id=uuid.uuid4(), memory_id=memory_id, json_messages=json.dumps(messages_data))
    db_session.add(db_entry)
    db_session.commit()
    
    retrieved_messages = chat_memory_store.get_messages(memory_id)
    assert retrieved_messages == messages_data

def test_get_messages_non_existing_id(chat_memory_store: PythonChatMemoryStore):
    retrieved_messages = chat_memory_store.get_messages("non_existent_mem")
    assert retrieved_messages == []

def test_update_messages_existing_id(chat_memory_store: PythonChatMemoryStore, db_session: Session):
    memory_id = "test_mem_3"
    initial_messages = [{"role": "user", "content": "First message"}]
    chat_memory_store.update_messages(memory_id, initial_messages) # This creates the initial entry
    
    updated_messages_data = [{"role": "user", "content": "First message"}, {"role": "ai", "content": "Second message"}]
    chat_memory_store.update_messages(memory_id, updated_messages_data) # This updates the existing entry
    
    entry = db_session.query(ChatMemoryModel).filter_by(memory_id=memory_id).first()
    assert entry is not None # Ensure entry still exists
    assert json.loads(entry.json_messages) == updated_messages_data

def test_delete_messages_existing_id(chat_memory_store: PythonChatMemoryStore, db_session: Session):
    memory_id = "test_mem_4"
    messages_data = [{"role": "user", "content": "To be deleted"}]
    # Use the store to create the message first
    chat_memory_store.update_messages(memory_id, messages_data)
    
    # Now delete it using the store
    chat_memory_store.delete_messages(memory_id)
    
    entry = db_session.query(ChatMemoryModel).filter_by(memory_id=memory_id).first()
    assert entry is None

def test_delete_messages_non_existing_id(chat_memory_store: PythonChatMemoryStore):
    # Should not raise an error
    try:
        chat_memory_store.delete_messages("non_existent_mem_del")
    except Exception as e:
        pytest.fail(f"Deleting non-existing memory ID raised an exception: {e}")
