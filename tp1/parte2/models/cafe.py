from pydantic import BaseModel
from typing import List, Optional


class Cafe(BaseModel):
    id: int
    nombre: str
    origen: str
    precio: float
    es_organico: bool = True


class GetCafesResponse(BaseModel):
    cafes: List[Cafe]


class CafeResponse(BaseModel):
    message: str