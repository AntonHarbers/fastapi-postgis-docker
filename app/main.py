from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from .database import engine, Base
from . import models
from .schemas import PointCreate

app = FastAPI()

DB_ENABLED = engine is not None

if DB_ENABLED: Base.metadata.create_all(bind = engine)

@app.get('/')
def root():
    return {"message" : "API Running from Github Actions deploy", "db_enabled": DB_ENABLED}

@app.get("/health")
def health():
    return {"ok" : True, "status" : "ok"}

@app.get('/db-test')
def db_test():
    if not DB_ENABLED:
        raise HTTPException(status_code=503, detail="Database not configured")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM points"))
        return {"db" : result}
    
@app.post('/points')
def create_point(point: PointCreate):
    if not DB_ENABLED:
        raise HTTPException(status_code=503, detail="Database not configured")

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
    if not DB_ENABLED:
        raise HTTPException(status_code=503, detail="Database not configured")
    
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