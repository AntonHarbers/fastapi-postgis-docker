from fastapi import FastAPI
from sqlalchemy import text
from .database import engine, Base

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
        result = conn.execute(text("SELECT 1"))
        return {"db" : result.scalar()}