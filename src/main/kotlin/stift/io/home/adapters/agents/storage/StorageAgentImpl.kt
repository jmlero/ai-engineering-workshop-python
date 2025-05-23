package stift.io.home.adapters.agents.storage

import dev.langchain4j.model.chat.ChatLanguageModel
import dev.langchain4j.service.AiServices
import org.springframework.stereotype.Service

// TODO: How does tool calling work in general? Using LangChain4J, how could you register tools?
@Service
class StorageAgentImpl(
    openaiLanguageModel: ChatLanguageModel,
) {
    val storageAgent: StorageAgent =
        AiServices.builder(StorageAgent::class.java)
            .chatLanguageModel(openaiLanguageModel)
//            .tools() // This is where you would register tools
//            .chatMemory() // This is where you would register a chat memory
            .build()

    fun call(request: String): String {
        return storageAgent.chat(request)
    }
}
