import uuid
from sqlalchemy import Column, String, Float
# Removed: from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as DB_UUID_type # For PostgreSQL
from sqlalchemy import Uuid as Default_UUID_type # Generic UUID type
from . import Base # Import shared Base

# Removed: Base = declarative_base()

class PantryModel(Base):
    __tablename__ = "pantry_entry"

    # Use Default_UUID_type for broader compatibility, can be overridden by DB specific later if needed
    id = Column(Default_UUID_type(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True) # Added index for name as it's often queried
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
