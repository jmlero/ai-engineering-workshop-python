package stift.io.home.infrastructure.llm

import dev.langchain4j.model.chat.ChatLanguageModel
import dev.langchain4j.model.openai.OpenAiChatModel
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration
class ChatLanguageModelConfig {
    @Bean
    fun openaiLanguageModel(openaiConfigurationProperties: OpenaiConfigurationProperties): ChatLanguageModel {
        return OpenAiChatModel.builder()
            .apiKey(openaiConfigurationProperties.apiKey)
            .modelName("gpt-4o-mini-2024-07-18")
            .temperature(0.0)
            .logRequests(true)
            .logResponses(true)
            .build()
    }
}