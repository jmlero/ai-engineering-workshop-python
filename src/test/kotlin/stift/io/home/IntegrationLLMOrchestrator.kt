package stift.io.home

import jakarta.annotation.PostConstruct
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import stift.io.home.adapters.LLMOrchestrator
import stift.io.home.evaluation.ResponseEvaluator
import kotlin.test.fail

@SpringBootTest
class IntegrationLLMOrchestrator {

    private lateinit var responseEvaluator: ResponseEvaluator
    @Autowired
    private lateinit var llmOrchestrator: LLMOrchestrator

    @PostConstruct
    fun setup() {
        responseEvaluator = ResponseEvaluator()
    }

    @Test
    fun `Whatever tests you feel are appropriate`() {
        // TODO: Think about how you could tes the llmOrchestrator
        fail("Not implemented")
    }
}
