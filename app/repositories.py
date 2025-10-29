from sqlmodel import select, Session
from typing import List, Optional
from .models import City


class CityRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[City]:
        statement = select(City)
        return self.session.exec(statement).all()

    def get_by_name(self, name: str) -> Optional[City]:
        statement = select(City).where(City.name == name)
        return self.session.exec(statement).first()

    def create(self, city: City) -> City:
        self.session.add(city)
        self.session.commit()
        self.session.refresh(city)
        return city

    def update(self, city: City) -> City:
        self.session.add(city)
        self.session.commit()
        self.session.refresh(city)
        return city

    def delete(self, city: City) -> None:
        self.session.delete(city)
        self.session.commit()