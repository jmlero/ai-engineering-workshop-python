package stift.io.home.adapters.pantry

import jakarta.persistence.*
import java.util.*

@Entity
@Table(name = "pantry_entry")
class PantryEntryEntity(
    @Id
    val id: UUID,
    @Column
    val name: String,
    @Column
    val quantity: Double,
    @Column
    val unit: String,
)
