package stift.io.home.adapters.chatmemory

import dev.langchain4j.data.message.ChatMessage
import dev.langchain4j.store.memory.chat.ChatMemoryStore
import dev.langchain4j.data.message.ChatMessageDeserializer.messagesFromJson
import dev.langchain4j.data.message.ChatMessageSerializer.messagesToJson
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Service
import java.util.*

// TODO: Figure out what this is good for. Why don't we just transmit everything from the FE? It has all messages, doesn't it?

@Service
class DurablyPersistedChatMemory(
    private val repo: ChatMemoryJpaRepository
) : ChatMemoryStore {

    companion object {
        val logger = LoggerFactory.getLogger(DurablyPersistedChatMemory::class.java)
    }

    override fun getMessages(memoryId: Any?): MutableList<ChatMessage> {
        assertString(memoryId)
        repo.findByMemoryId(memoryId as String)?.let {
            return messagesFromJson(it.json)
        } ?: run {
            logger.info("Creating ChatMemory for $memoryId")
            return mutableListOf()
        }
    }

    override fun updateMessages(memoryId: Any?, messages: MutableList<ChatMessage>?) {
        assertString(memoryId)
        repo.findByMemoryId(memoryId as String)?.let {
            repo.save(ChatMemoryEntity(id = it.id, memoryId = memoryId, json = messagesToJson(messages)))
        } ?: run {
            repo.save(ChatMemoryEntity(id = UUID.randomUUID(), memoryId = memoryId, json = messagesToJson(messages)))
        }
    }

    override fun deleteMessages(memoryId: Any?) {
        assertString(memoryId)
        repo.findByMemoryId(memoryId as String)?.let {
            repo.delete(it)
        }
    }

    private fun assertString(it: Any?) {
        if (it !is String) throw IllegalArgumentException("Expected String but found ${it?.javaClass}")
    }
}
