from python_app.agents.storage_agent import PythonStorageAgent

class PythonLLMOrchestrator:
    def __init__(self, storage_agent: PythonStorageAgent):
        self.storage_agent = storage_agent

    def call(self, request: str) -> str:
        return self.storage_agent.chat(request)
