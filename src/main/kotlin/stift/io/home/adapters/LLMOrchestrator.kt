package stift.io.home.adapters

import org.springframework.stereotype.Service
import stift.io.home.adapters.agents.storage.StorageAgentImpl

// TODO: Doesn't orchestrate much as of now - we only have one agent 🤷‍♂️
// TODO: But think: What are the reasons to break functionality up into multiple agents?
@Service
class LLMOrchestrator(
    private val storageAgent: StorageAgentImpl,
) {
    fun call(request: String): String {
        return this.storageAgent.call(
            request = request
        )
    }
}
