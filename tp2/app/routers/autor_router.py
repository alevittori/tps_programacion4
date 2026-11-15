from typing import Sequence
from fastapi import APIRouter, HTTPException, status
from app.dependencies import AutorServiceDep
from app.models.autor import Autor, AutorCreate, AutorUpdate

router = APIRouter(prefix="/autores", tags=["Autores"])

@router.post("/", response_model=Autor, status_code=status.HTTP_201_CREATED)
def crear_autor(autor_in: AutorCreate, service: AutorServiceDep) -> Autor:
    return service.create_autor(autor_in)

@router.get("/", response_model=Sequence[Autor])
def listar_autores(service: AutorServiceDep, skip: int = 0, limit: int = 100) -> Sequence[Autor]:
    return service.get_autores(skip, limit)

@router.get("/{autor_id}", response_model=Autor)
def obtener_autor(autor_id: int, service: AutorServiceDep) -> Autor:
    autor = service.get_autor_by_id(autor_id)
    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autor no encontrado"
        )
    return autor

@router.put("/{autor_id}", response_model=Autor)
def actualizar_autor(autor_id: int, autor_in: AutorUpdate, service: AutorServiceDep) -> Autor:
    autor = service.update_autor(autor_id, autor_in)
    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autor no encontrado"
        )
    return autor

@router.delete("/{autor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_autor(autor_id: int, service: AutorServiceDep):
    success = service.delete_autor(autor_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autor no encontrado"
        )
        
    return None