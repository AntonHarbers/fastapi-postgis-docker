from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True) if DATABASE_URL else None

SessionLocal = sessionmaker(bind = engine) if engine else None

class Base(DeclarativeBase): pass