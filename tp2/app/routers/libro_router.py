from typing import Sequence
from fastapi import APIRouter, HTTPException, status
from app.dependencies import LibroServiceDep
from app.models.libro import Libro, LibroCreate, LibroUpdate

router = APIRouter(prefix="/libros", tags=["Libros"])

@router.post("/", response_model=Libro, status_code=status.HTTP_201_CREATED)
def crear_libro(libro_in: LibroCreate, service: LibroServiceDep) -> Libro:
    try:
        return service.create_libro(libro_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=Sequence[Libro])
def listar_libros(service: LibroServiceDep, skip: int = 0, limit: int = 100) -> Sequence[Libro]:
    return service.get_libros(skip, limit)

@router.get("/{libro_id}", response_model=Libro)
def obtener_libro(libro_id: int, service: LibroServiceDep) -> Libro:
    libro = service.get_libro_by_id(libro_id)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado"
        )
    return libro

@router.put("/{libro_id}", response_model=Libro)
def actualizar_libro(libro_id: int, libro_in: LibroUpdate, service: LibroServiceDep) -> Libro:
    libro = service.update_libro(libro_id, libro_in)
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado"
        )
    return libro

@router.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(libro_id: int, service: LibroServiceDep):
    success = service.delete_libro(libro_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado"
        )
    return None

@router.post("/{libro_id}/autores/{autor_id}", response_model=Libro, status_code=status.HTTP_200_OK)
def asociar_autor_a_libro(libro_id: int, autor_id: int, service: LibroServiceDep) -> Libro:
    try:
        return service.asociar_autor(libro_id=libro_id, autor_id=autor_id)
    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
@router.delete("/{libro_id}/autores/{autor_id}", response_model=Libro, status_code=status.HTTP_200_OK)
def desasociar_autor_de_libro(libro_id: int, autor_id: int, service: LibroServiceDep) -> Libro:
    try:
        return service.desasociar_autor(libro_id=libro_id, autor_id=autor_id)
    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )