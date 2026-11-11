from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from models.cafe import Cafe, GetCafesResponse, CafeResponse

router = APIRouter()


cafes: List[Cafe] = [
    Cafe(id=1, nombre="Colombia Supremo", origen="Colombia", precio=12500.0, es_organico=True),
    Cafe(id=2, nombre="Tarrazú Especial", origen="Costa Rica", precio=14200.0, es_organico=False),
]


# LISTAR y FILTRAR (si es orgánico)
@router.get("/cafe", response_model=GetCafesResponse)
def get_cafes(
    es_organico: Optional[bool] = None
) -> GetCafesResponse:
    resultado = cafes

    if es_organico is not None:
        resultado = [cafe for cafe in resultado if cafe.es_organico == es_organico]

    return GetCafesResponse(cafes=resultado)


#  OBTENER POR ID
@router.get("/cafe/{id}", response_model=Cafe)
def get_cafe_by_id(id: int) -> Cafe:
    for cafe in cafes:
        if cafe.id == id:
            return cafe

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Café no encontrado"
    )


# CREAR
@router.post("/cafe", status_code=status.HTTP_201_CREATED, response_model=CafeResponse)
def create_cafe(cafe: Cafe) -> CafeResponse:
    for existing_cafe in cafes:
        if existing_cafe.id == cafe.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El ID de café ya existe"
            )
            
    cafes.append(cafe)
    return CafeResponse(message="Café creado con éxito")


# MODIFICAR (actualiza propiedades conservando el ID original)
@router.put("/cafe/{id}", response_model=CafeResponse)
def update_cafe(id: int, cafe_actualizado: Cafe) -> CafeResponse:
    for cafe in cafes:
        if cafe.id == id:
            cafe.nombre = cafe_actualizado.nombre
            cafe.origen = cafe_actualizado.origen
            cafe.precio = cafe_actualizado.precio
            cafe.es_organico = cafe_actualizado.es_organico
            
            return CafeResponse(message="Café actualizado con éxito")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Café no encontrado"
    )


# ELIMINAR
@router.delete("/cafe/{id}", response_model=CafeResponse)
def delete_cafe(id: int) -> CafeResponse:
    for cafe in cafes:
        if cafe.id == id:
            cafes.remove(cafe)
            return CafeResponse(message="Café eliminado con éxito")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Café no encontrado"
    )