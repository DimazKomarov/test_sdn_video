from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlmodel import Session

from .schemas import CityCreate, CityRead
from .models import City
from .database import get_session
from .repositories import CityRepository
from .services import geocode_city
from .utils import haversine

router = APIRouter()


@router.post("/cities", response_model=CityRead)
async def create_city(payload: CityCreate, session: Session = Depends(get_session)):
    repo = CityRepository(session)
    name = payload.name
    if not name:
        raise HTTPException(status_code=400, detail=f"Field '{name}' is required")

    coords = await geocode_city(name)
    if coords is None:
        raise HTTPException(status_code=404, detail=f"Coordinates for '{name}' not found")

    existing = repo.get_by_name(name)
    if existing:
        existing.lat = coords["lat"]
        existing.lon = coords["lon"]
        updated = repo.update(existing)
        return updated

    city = City(name=name, lat=coords["lat"], lon=coords["lon"])
    created = repo.create(city)
    return created


@router.delete("/cities/{name}")
def delete_city(name: str, session: Session = Depends(get_session)):
    repo = CityRepository(session)
    existing = repo.get_by_name(name)
    if not existing:
        raise HTTPException(status_code=404, detail="City not found")
    repo.delete(existing)
    return {"detail": f"City '{name}' deleted"}


@router.get("/cities", response_model=List[CityRead])
def list_cities(session: Session = Depends(get_session)):
    repo = CityRepository(session)
    return repo.get_all()


@router.get("/nearest", response_model=List[CityRead])
def nearest(lat: float = Query(...), lon: float = Query(...), session: Session = Depends(get_session)):
    repo = CityRepository(session)
    cities = repo.get_all()
    if not cities:
        return []
    arr = []
    for c in cities:
        d = haversine(lat, lon, c.lat, c.lon)
        arr.append((d, c))
    arr.sort(key=lambda x: x[0])
    nearest_two = [item[1] for item in arr[:2]]
    return nearest_two