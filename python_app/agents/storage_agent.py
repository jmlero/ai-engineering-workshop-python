from langchain_core.chat_models.base import BaseChatModel # Updated to langchain_core
from langchain_community.chat_models.fake import FakeListChatModel
from langchain_core.messages import SystemMessage, HumanMessage # Updated to langchain_core

class PythonStorageAgent:
    SYSTEM_PROMPT = "If prompted, tell the user that you're confused and don't quite know who or what you are. They should help you understand that better by providing you with a proper system prompt."

    def __init__(self, chat_model: BaseChatModel):
        self.chat_model = chat_model

    def chat(self, user_message: str) -> str:
        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=user_message)
        ]
        # .invoke is for LCEL, for older model API, it might be .predict_messages or similar
        # For FakeListChatModel, .invoke should work with a list of messages.
        # Or using .generate([messages])
        response = self.chat_model.invoke(messages) 
        return response.content
