package stift.io.home.adapters.chatmemory

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository

@Repository
interface ChatMemoryJpaRepository : JpaRepository<ChatMemoryEntity, String> {
    fun findByMemoryId(memoryId: String): ChatMemoryEntity?
}