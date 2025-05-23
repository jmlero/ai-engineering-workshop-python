from typing import List
import uuid # Required for PantryEntry id type hint if not already imported by PantryEntry
from sqlalchemy.orm import Session
from ..models.pantry_model import PantryModel
from ..services.pantry_service import DurablePantry, PantryEntry

class SqlAlchemyDurablePantryAdapter(DurablePantry):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, model: PantryModel) -> PantryEntry:
        """Helper method to convert SQLAlchemy model to domain object."""
        return PantryEntry(id=model.id, name=model.name, amount=model.quantity, unit=model.unit)

    def find_all(self) -> List[PantryEntry]:
        all_models = self.session.query(PantryModel).all()
        return [self._to_domain(model) for model in all_models]

    def find_all_where_names_exist(self, names: List[str]) -> List[PantryEntry]:
        if not names: # Handle empty list of names to avoid issues with IN clause
            return []
        models = self.session.query(PantryModel).filter(PantryModel.name.in_(names)).all()
        return [self._to_domain(model) for model in models]

    def save_all(self, entries: List[PantryEntry]) -> List[PantryEntry]:
        saved_domain_entries = []
        
        # Process entries to update existing or add new ones
        # It's more efficient to fetch all potentially existing models in one query
        entry_ids = [entry.id for entry in entries if entry.id is not None]
        existing_models_map = {}
        if entry_ids:
            existing_models = self.session.query(PantryModel).filter(PantryModel.id.in_(entry_ids)).all()
            existing_models_map = {model.id: model for model in existing_models}

        for entry_data in entries:
            model = existing_models_map.get(entry_data.id)
            
            if model:
                # Update existing model
                model.name = entry_data.name
                model.quantity = entry_data.amount
                model.unit = entry_data.unit
            else:
                # Create new model instance
                # Ensure id is a UUID object if it's coming as a string
                model_id = entry_data.id if isinstance(entry_data.id, uuid.UUID) else uuid.UUID(str(entry_data.id))
                model = PantryModel(
                    id=model_id, 
                    name=entry_data.name, 
                    quantity=entry_data.amount, 
                    unit=entry_data.unit
                )
                self.session.add(model)
            # The model added or updated will be part of the session's transaction.
            # We will convert back to domain object after commit.
        
        self.session.commit()

        # After commit, IDs are finalized (especially for new entries if not client-generated).
        # Re-fetch or use the current model instances to convert back to domain objects.
        # For this implementation, we'll assume the models in session are up-to-date.
        # A more robust way for newly created items (if ID was server generated) would be to re-fetch.
        # However, since we generate UUIDs on the client (PantryEntry default_factory or here),
        # the IDs are known before commit.

        # To ensure we return the state as it is in the database (e.g., after triggers or defaults),
        # it's good practice to get the entities from the session or database again.
        # For simplicity and given client-side UUIDs, we'll convert the current model states.
        
        # We need to get the actual model objects that were saved or updated to return their domain representations.
        # The `entries` list contains domain objects. We need to map them to the corresponding
        # SQLAlchemy models that are now in the session and committed.
        
        # Let's collect all model IDs from the input entries
        all_entry_ids = [entry.id for entry in entries]
        
        # Fetch these models from the database again to ensure we have the committed state
        # This is the safest way to ensure the returned data is accurate.
        if all_entry_ids:
            committed_models = self.session.query(PantryModel).filter(PantryModel.id.in_(all_entry_ids)).all()
            saved_domain_entries = [self._to_domain(model) for model in committed_models]
        else:
            saved_domain_entries = []
            
        return saved_domain_entries
