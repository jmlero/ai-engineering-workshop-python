package stift.io.home.config

import java.io.File
import java.util.*

class TestSecrets {
    companion object {
        private val properties = Properties().apply {
            val envFiles = listOf(
                File("../.env"),
                File(".env"),
                File("server/.env")
            )

            val envFile = envFiles.find { it.exists() }
                ?: throw IllegalStateException("No .env file found in any of the expected locations")

            load(envFile.inputStream())
        }

        fun openAiToken(): String {
            return properties.getProperty("OPENAI_API_KEY")
                ?: throw IllegalStateException("OPENAI_API_KEY not found in .env file")
        }
    }
}