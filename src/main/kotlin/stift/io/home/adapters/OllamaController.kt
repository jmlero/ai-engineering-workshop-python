package stift.io.home.adapters

import jakarta.servlet.http.HttpServletRequest
import org.slf4j.LoggerFactory
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import java.io.BufferedReader
import java.time.LocalDateTime

/*
 * This is an interface supposed to mock the minimum an interface like WebUI needs to
 * allow us to focus on the LLM side of things instead of the UI. The only method you
 * really have to pay attention to is @chatRequest()
 */
@RestController
class OllamaController(
    val llmController: LLMOrchestrator
) {
    @RequestMapping("/ollama/**")
    fun handleRequest(request: HttpServletRequest): ResponseEntity<Any> {
        // Log incoming requests that hit unknown endpoints
        logger.info("GENERAL")
        logger.info(map(request))
        return ResponseEntity.unprocessableEntity().build()
    }

    @GetMapping("/ollama/")
    fun getHeartbeat() {
        logger.info("HEARTBEAT")
    }

    @PostMapping("/ollama/api/chat")
    fun chatRequest(@RequestBody request: OllamaChatRequest): OllamaChatResponse {
        val lastMessage = request.messages.last()
        val reply = llmController.call(lastMessage.content)

        return OllamaChatResponse(
                Message(
                        role = "system",
                        content = reply,
                        images = listOf(),
                        tool_calls = listOf()
                ),
                model = "workshop",
                created_at = LocalDateTime.now(),
                done = true,
                done_reason = "stop",
                total_duration = 5589157167,
                load_duration = 3013701500,
                prompt_eval_count = 50,
                prompt_eval_duration = 2000,
                eval_count = 200,
                eval_duration = 1325948000
        )
    }

    @GetMapping("/ollama/api/tags")
    fun getTags(): TagsResponse {
        return TagsResponse(
            models = listOf(
                ModelInfo(
                    name = "workshop:latest",
                    model = "workshop:latest",
                    modified_at = LocalDateTime.now().toString(),
                    size = 3817517056,
                    digest = "sha256:mock",
                    details = ModelDetails(
                        format = "gguf",
                        family = "workshop",
                        parameter_size = "7B",
                        quantization_level = "Q4_K_M"
                    )
                )
            )
        )
    }

    @GetMapping("/api/models")
    fun getModels(): Map<String, List<Map<String, Any>>> {
        return mapOf(
            "models" to listOf(
                mapOf(
                    "id" to "workshop:latest",
                    "model" to "workshop:latest",
                    "name" to "workshop:latest",
                    "modified_at" to LocalDateTime.now().toString(),
                    "size" to 3817517056,
                    "digest" to "sha256:mock",
                    "details" to mapOf(
                        "format" to "gguf",
                        "family" to "workshop",
                        "parameter_size" to "7B",
                        "quantization_level" to "Q4_K_M"
                    )
                )
            )
        )
     }

    @GetMapping("/ollama/api/version")
    fun getVersion(): Map<String, String> {
        return mapOf(
            "version" to "0.0.1",
            "build" to "latest"
        )
    }

    private fun map(request: HttpServletRequest): String {
        val method = request.method
        val path = request.requestURI
        val queryString = request.queryString ?: ""

        val body = request.reader.use(BufferedReader::readText)
        val headers =
                request.headerNames.toList().associate { name -> name to request.getHeader(name) }

        return """
            Method: $method
            Path: $path
            Query: $queryString
            Headers: $headers
            Body: $body
        """.trimIndent()
    }

    companion object {
        val logger = LoggerFactory.getLogger(OllamaController::class.java)
    }
}

data class OllamaChatResponse(
        val message: Message,
        val model: String,
        val created_at: LocalDateTime,
        val done: Boolean,
        val done_reason: String,
        val total_duration: Long,
        val load_duration: Long,
        val prompt_eval_count: Long,
        val prompt_eval_duration: Long,
        val eval_count: Long,
        val eval_duration: Long
)

data class Message(
        val role: String,
        val content: String,
        val images: List<String>?,
        val tool_calls: List<ToolCall>?
)

data class ToolCall(val function: Function)

data class Function(val name: String, val arguments: Map<String, Any>)

data class OllamaChatRequest(
        val stream: Boolean,
        val messages: List<Message>,
        val options: ChatOptions?,
        val model: String
)

data class ChatOptions(val temperature: Int)

data class TagsResponse(
    val models: List<ModelInfo>
)

data class ModelInfo(
    val name: String,
    val model: String,
    val modified_at: String,
    val size: Long,
    val digest: String,
    val details: ModelDetails
)

data class ModelDetails(
    val format: String,
    val family: String,
    val parameter_size: String,
    val quantization_level: String
)
