from sqlalchemy import Column, Integer, text, String
from .database import Base
from geoalchemy2 import Geometry

class Point(Base):
    __tablename__ = "points"
    id = Column(Integer, primary_key=True, index=True)
    geom = Column(Geometry("POINT", srid=4326))
    name = Column(String, nullable=False)