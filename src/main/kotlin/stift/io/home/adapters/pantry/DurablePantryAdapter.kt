package stift.io.home.adapters.pantry

import org.springframework.stereotype.Service
import stift.io.home.domain.DurablePantry
import stift.io.home.domain.PantryService

@Service
class DurablePantryAdapter(
    private val repo: PantryJpaRepository,
) : DurablePantry {
    override fun findAll(): List<PantryService.PantryEntry> {
        return repo.findBy().map {
            return@map PantryService.PantryEntry(
                id = it.id,
                name = it.name,
                amount = it.quantity,
                unit = it.unit,
            )
        }
    }

    override fun findAllWhereNamesExist(
        names: List<String>
    ): List<PantryService.PantryEntry> {
        return repo.findAllByNameIsIn(names)
            .map { entry ->
                PantryService.PantryEntry(
                    id = entry.id,
                    name = entry.name,
                    amount = entry.quantity,
                    unit = entry.unit,
                )
            }
    }

    override fun saveAll(
        entries: List<PantryService.PantryEntry>
    ): List<PantryService.PantryEntry> {
        return repo.saveAll(
            entries.map { entryCandidate ->
                PantryEntryEntity(
                    id = entryCandidate.id,
                    name = entryCandidate.name,
                    quantity = entryCandidate.amount,
                    unit = entryCandidate.unit,
                )
            }
        ).map { savedEntity ->
                PantryService.PantryEntry(
                    id = savedEntity.id,
                    name = savedEntity.name,
                    amount = savedEntity.quantity,
                    unit = savedEntity.unit,
                )
            }
    }
}
