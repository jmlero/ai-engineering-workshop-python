import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID # For later, if we use postgres
# Removed: from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker # Keep for example, though not used by model directly
from sqlalchemy.types import TypeDecorator, CHAR # Keep for example
import sqlalchemy # For sqlalchemy.UUID
from . import Base # Import shared Base

# Using sqlalchemy.UUID which is database agnostic for UUID type
# For SQLite, it will store as CHAR(32) by default if as_uuid=False,
# or requires custom type if as_uuid=True without native UUID support.
# For simplicity with SQLite and to ensure UUID objects are used,
# we can use as_uuid=True and rely on SQLAlchemy's handling or define a custom type.
# However, standard sqlalchemy.UUID(as_uuid=True) should work.

# Removed: Base = declarative_base()

class ChatMemoryModel(Base):
    __tablename__ = "chat_memory"

    id = Column(sqlalchemy.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    memory_id = Column(String, unique=True, index=True, nullable=False)
    json_messages = Column(Text, nullable=False)

# Example of how to create an engine and session (not for direct use here but for context)
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# from sqlalchemy import create_engine # Add import for example
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine) # To create tables
