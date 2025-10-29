from pydantic import BaseModel


class CityCreate(BaseModel):
    name: str


class CityRead(BaseModel):
    id: int
    name: str
    lat: float
    lon: float

    class Config:
        from_attributes = True