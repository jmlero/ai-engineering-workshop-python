package stift.io.home.domain

import dev.langchain4j.agent.tool.Tool
import java.util.*
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Service

// TODO: We want the LLM to be able to use methods on this class. How can we provide them? (Hint: @Tool())
// TODO: Assuming we had User Entities and Spring Security - how could we retain the UserContext on a path through an LLM?
// TODO: How can we do that safely?
interface DurablePantry {
    fun findAll(): List<PantryService.PantryEntry>
    fun findAllWhereNamesExist(
        names: List<String>
    ): List<PantryService.PantryEntry>

    fun saveAll(entries: List<PantryService.PantryEntry>): List<PantryService.PantryEntry>
}

@Service
class PantryService(
    private val durablePantry: DurablePantry,
) {
    data class LineItem(val name: String, val amount: Double, val unit: String)

    data class StorageRequest(val items: List<LineItem>)

    data class UseFoodRequest(val items: List<LineItem>)

    data class PantryEntry(
        val id: UUID,
        val name: String,
        val amount: Double,
        val unit: String
    )

    fun saveFood(request: StorageRequest): List<PantryEntry> {
        logger.info("Incoming save food Request: $request")
        val saveRequestList = request.items
        val existingEntries =
            durablePantry.findAllWhereNamesExist(request.items.map { it.name })

        val updateList =
            saveRequestList.map { entryToSave ->
                existingEntries
                    .find { it.name == entryToSave.name }
                    ?.copy(amount = entryToSave.amount, unit = entryToSave.unit)
                    ?: PantryEntry(
                        id = UUID.randomUUID(),
                        name = entryToSave.name,
                        amount = entryToSave.amount,
                        unit = entryToSave.unit
                    )
            }

        val savedEntries = durablePantry.saveAll(updateList)

        return savedEntries
    }

    fun useFood(request: UseFoodRequest): List<PantryEntry> {
        logger.info("Incoming use food Request: $request")
        val existingEntries =
            durablePantry.findAllWhereNamesExist(request.items.map { it.name })

        val updatedEntries =
            request.items.mapNotNull { itemToUse ->
                existingEntries
                    .find { it.name == itemToUse.name }
                    ?.let { existingItem ->
                        val newAmount = maxOf(0.0, existingItem.amount - itemToUse.amount)
                        existingItem.copy(amount = newAmount)
                    }
                    ?.also {
                        if (it.amount == 0.0) {
                            logger.info("Item ${it.name} is now depleted")
                        }
                    }
                    ?: run {
                        logger.error("Item not in storage: ${itemToUse.name}")
                        null
                    }
            }

        val savedEntries =
            if (updatedEntries.isNotEmpty()) {
                durablePantry.saveAll(updatedEntries)
            } else {
                emptyList()
            }

        return savedEntries
    }

    fun getFood(): List<PantryEntry> {
        return durablePantry.findAll()
    }

    companion object {
        private val logger = LoggerFactory.getLogger(this::class.java)
    }
}
