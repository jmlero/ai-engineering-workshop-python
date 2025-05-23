package stift.io.home.evaluation

import dev.langchain4j.data.message.ChatMessage
import dev.langchain4j.data.message.SystemMessage
import dev.langchain4j.data.message.TextContent
import dev.langchain4j.data.message.UserMessage
import dev.langchain4j.model.openai.OpenAiChatModel
import stift.io.home.config.TestSecrets

// TODO: This will be useful. Jumping between the probabilistic space of LLMs to the deterministic space of tests is a difficult bridge to cross.
// TODO: As strange as it seems, evaluating agents (aka LLMs evaluating LLMs) have emerged as a promising approach.
class ResponseEvaluator() {
    private val languageModel =
        OpenAiChatModel.builder()
            .apiKey(TestSecrets.openAiToken())
            .modelName("gpt-4o-mini-2024-07-18")
            .temperature(0.0)
            .build()

    /**
     * Evaluates if a given response conforms to an expected truth condition
     * @param expectedTruth The truth condition that should be met
     * @param responses List of all responses in the conversation
     * @return "true" or the explanation why it isn't true
     */
    fun evaluateResponse(expectedTruth: String, responses: List<String>): String {
        println("Conversation: $responses")

        val messages = createEvaluationMessages(expectedTruth, responses.last())
        val result = languageModel.generate(messages.first(), messages.last())
        val text = result.content().text().trim()
        return if (text.lowercase() == "true") {
            "true"
        } else {
            text
        }
    }

    private fun createEvaluationMessages(truth: String, response: String): List<ChatMessage> {
        val system =
            SystemMessage(
                "The current state of the world is: '$truth', return true if the following statement conforms to the truth. IMPORTANT: Only stray from returning 'true' if the statement is incorrect. Explain why if that is the case."
            )
        val toBeTested = UserMessage(TextContent(response))
        return listOf(system, toBeTested)
    }
}
