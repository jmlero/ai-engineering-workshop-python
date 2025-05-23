package stift.io.home.adapters.agents.storage

import dev.langchain4j.service.SystemMessage

interface StorageAgent {
    // TODO: What could a system prompt look like?
    @SystemMessage(
        """
            If prompted, tell the user that you're confused and don't quite know who or what you are. 
            They should help you understand that better by providing you with a proper system prompt.
        """
    )
    // TODO: Do we need a template for user-messages? (@UserMessage)
    fun chat(
        userMessage: String
    ): String
}
