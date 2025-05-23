import abc
import dataclasses
import logging
import uuid
from typing import List

logger = logging.getLogger(__name__)

@dataclasses.dataclass
class LineItem:
    name: str
    amount: float
    unit: str

@dataclasses.dataclass
class PantryEntry:
    id: uuid.UUID = dataclasses.field(default_factory=uuid.uuid4)
    name: str
    amount: float
    unit: str

@dataclasses.dataclass
class StorageRequest:
    items: List[LineItem]

@dataclasses.dataclass
class UseFoodRequest:
    items: List[LineItem]

class DurablePantry(abc.ABC):
    @abc.abstractmethod
    def find_all(self) -> List[PantryEntry]:
        pass

    @abc.abstractmethod
    def find_all_where_names_exist(self, names: List[str]) -> List[PantryEntry]:
        pass

    @abc.abstractmethod
    def save_all(self, entries: List[PantryEntry]) -> List[PantryEntry]:
        pass

class PantryService:
    def __init__(self, durable_pantry: DurablePantry):
        self.durable_pantry = durable_pantry

    def get_food(self) -> List[PantryEntry]:
        logger.info("Finding all pantry entries")
        return self.durable_pantry.find_all()

    def save_food(self, request: StorageRequest) -> List[PantryEntry]:
        logger.info(f"Saving food items: {request.items}")
        
        names_to_find = [item.name for item in request.items]
        existing_entries = self.durable_pantry.find_all_where_names_exist(names_to_find)
        
        existing_map = {entry.name: entry for entry in existing_entries}
        
        updated_entries = []
        new_entries = []

        for item in request.items:
            if item.name in existing_map:
                entry = existing_map[item.name]
                if entry.unit != item.unit:
                    logger.error(f"Unit mismatch for {item.name}: existing {entry.unit}, new {item.unit}")
                    raise ValueError(f"Unit mismatch for {item.name}")
                entry.amount = item.amount # Changed from += to =
                updated_entries.append(entry)
            else:
                new_entries.append(PantryEntry(name=item.name, amount=item.amount, unit=item.unit))
        
        saved_entries = self.durable_pantry.save_all(updated_entries + new_entries)
        logger.info(f"Saved entries: {saved_entries}")
        return saved_entries

    def use_food(self, request: UseFoodRequest) -> List[PantryEntry]:
        logger.info(f"Using food items: {request.items}")

        names_to_find = [item.name for item in request.items]
        existing_entries = self.durable_pantry.find_all_where_names_exist(names_to_find)
        
        existing_map = {entry.name: entry for entry in existing_entries}
        
        entries_to_save = []

        for item in request.items:
            if item.name not in existing_map:
                logger.error(f"Item not found in pantry: {item.name}")
                # Removed: raise ValueError(f"Item not found: {item.name}")
                continue # Skip to the next item

            entry = existing_map[item.name]
            if entry.unit != item.unit:
                logger.error(f"Unit mismatch for {item.name}: existing {entry.unit}, requested {item.unit}")
                raise ValueError(f"Unit mismatch for {item.name}")
            
            if entry.amount < item.amount:
                logger.error(f"Not enough {item.name} in pantry: requested {item.amount}, available {entry.amount}")
                raise ValueError(f"Not enough {item.name}")

            entry.amount -= item.amount
            entries_to_save.append(entry)
            
        saved_entries = self.durable_pantry.save_all(entries_to_save)
        logger.info(f"Updated entries after use: {saved_entries}")
        return saved_entries
