package stift.io.home.adapters.chatmemory

import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.Id
import jakarta.persistence.Table
import java.util.*

@Entity
@Table(name = "chat_memory")
class ChatMemoryEntity(
    @Id
    val id: UUID,
    @Column
    val memoryId: String,
    @Column(columnDefinition = "CLOB")
    val json: String,
)
