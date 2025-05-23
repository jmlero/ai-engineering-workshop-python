package stift.io.home.adapters.pantry

import java.util.*
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository

@Repository
interface PantryJpaRepository : JpaRepository<PantryEntryEntity, UUID> {
    fun findAllByNameIsIn(name: List<String>): List<PantryEntryEntity>
    fun findBy(): List<PantryEntryEntity>
}
