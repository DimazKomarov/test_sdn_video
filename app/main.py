from fastapi import FastAPI
from .database import init_db
from .routers import router as city_router

app = FastAPI(title="Cities API")

app.include_router(city_router)

@app.on_event("startup")
def on_startup():
    init_db()
