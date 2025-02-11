"""DB configuration"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database URL
DATABASE_URL = "sqlite:///shadowing.db"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a sessionfactory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class for the models
Base = declarative_base()
