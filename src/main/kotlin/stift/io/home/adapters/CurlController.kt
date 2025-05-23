package stift.io.home.adapters

import jakarta.servlet.http.HttpServletRequest
import org.slf4j.LoggerFactory
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import java.io.BufferedReader
import java.time.LocalDateTime

/*
 * This interface provides a very simple entrypoint into the application for use when WebUI is not easily available.
 */
@RestController
class CurlController(
    val llmController: LLMOrchestrator
) {
    @PostMapping("/curl/chat")
    fun chatRequest(@RequestBody request: CurlChatRequest): String {
        logger.info("Incoming request: $request")
        return llmController.call(request.message)
    }

    companion object {
        val logger = LoggerFactory.getLogger(OllamaController::class.java)
    }
}

data class CurlChatRequest(
    val message: String
)
