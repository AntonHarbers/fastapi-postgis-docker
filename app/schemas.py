from pydantic import BaseModel

class PointCreate(BaseModel):
    lat: float
    lon: float
    name: str