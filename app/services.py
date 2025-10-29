import httpx
from typing import Optional
from .config import NOMINATIM_USER_AGENT

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


async def geocode_city(name: str) -> Optional[dict]:
    params = {"q": name, "format": "json", "limit": 1}
    headers = {"User-Agent": NOMINATIM_USER_AGENT}
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(NOMINATIM_URL, params=params, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None
        first = data[0]
        return {"lat": float(first["lat"]), "lon": float(first["lon"])}