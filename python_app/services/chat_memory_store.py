import json
from typing import List
from sqlalchemy.orm import Session
from ..models.chat_memory_model import ChatMemoryModel

class PythonChatMemoryStore:
    def __init__(self, session: Session):
        self.session = session

    def get_messages(self, memory_id: str) -> List[dict]:
        entry = self.session.query(ChatMemoryModel).filter_by(memory_id=memory_id).first()
        if entry:
            return json.loads(entry.json_messages)
        return []

    def update_messages(self, memory_id: str, messages: List[dict]):
        json_messages_str = json.dumps(messages)
        entry = self.session.query(ChatMemoryModel).filter_by(memory_id=memory_id).first()
        if entry:
            entry.json_messages = json_messages_str
        else:
            new_entry = ChatMemoryModel(memory_id=memory_id, json_messages=json_messages_str)
            self.session.add(new_entry)
        self.session.commit()

    def delete_messages(self, memory_id: str):
        entry = self.session.query(ChatMemoryModel).filter_by(memory_id=memory_id).first()
        if entry:
            self.session.delete(entry)
            self.session.commit()
