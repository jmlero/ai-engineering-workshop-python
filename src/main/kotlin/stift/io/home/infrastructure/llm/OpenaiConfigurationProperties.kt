package stift.io.home.infrastructure.llm

import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.boot.context.properties.bind.ConstructorBinding

@ConfigurationProperties(prefix = "application.llm.openai")
data class OpenaiConfigurationProperties @ConstructorBinding constructor(
    val apiKey: String,
)