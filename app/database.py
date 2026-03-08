from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@db:5432/fastapi_demo")

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind = engine)

class Base(DeclarativeBase): pass