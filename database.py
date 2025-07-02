from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker  #there has to b session in which database is connected 

SQLALCHEMY_DATABASE_URL = "sqlite:///./product.db"  # SQLite database URL
engine=create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False })  # Create the engine with connection arguments for SQLite

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)  # Create a session factory
Base= declarative_base()  # Create a base class for declarative models

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()