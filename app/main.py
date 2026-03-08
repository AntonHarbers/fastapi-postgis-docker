from fastapi import FastAPI
from sqlalchemy import text
from .database import engine, Base
from . import models
from .schemas import PointCreate

app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.get('/')
def root():
    return {"message" : "API Running"}

@app.get("/health")
def health():
    return {"ok" : True, "status" : "ok"}

@app.get('/db-test')
def db_test():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM points"))
        return {"db" : result}
    
@app.post('/points')
def create_point(point: PointCreate):
    query = text("""
                INSERT INTO points (name, geom)
                VALUES (:name, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326))
                RETURNING id 
                """)

    with engine.begin() as conn:
        result = conn.execute(query, {
            "lon" : point.lon,
            "lat": point.lat,
            "name": point.name
        })
        point_id = result.scalar()
    
    return {"id": point_id}

@app.get("/points/nearby")
def nearby_points(lon: float, lat: float):
    query = text("""
        SELECT id, name,
        ST_Distance(
                 geom::geography, 
                 ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography
                 ) AS distance
                 FROM points
                 ORDER BY geom <-> ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
                 LIMIT 10

    """)

    with engine.connect() as conn:
        result = conn.execute(query, {
            "lon": lon, "lat": lat
        })
    
        rows = [
            {"id" : r.id, "distance": r.distance, "name": r.name} for r in result
        ]

    
    return rows