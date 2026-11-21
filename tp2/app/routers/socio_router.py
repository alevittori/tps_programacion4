from typing import Sequence
from fastapi import APIRouter, HTTPException, status
from app.dependencies import PrestamoServiceDep, SocioServiceDep
from app.models.socio import Socio, SocioCreate, SocioUpdate
from app.models.prestamo import Prestamo

router = APIRouter(prefix="/socios", tags=["Socios"])

@router.post("/", response_model=Socio, status_code=status.HTTP_201_CREATED)
def crear_socio(socio_in: SocioCreate, service: SocioServiceDep) -> Socio:
    try:
        return service.create_socio(socio_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.get("/", response_model=Sequence[Socio])
def listar_socios(service: SocioServiceDep, skip: int = 0, limit: int = 100) -> Sequence[Socio]:
    return service.get_socios(skip, limit)

@router.get("/{socio_id}", response_model=Socio)
def obtener_socio(socio_id: int, service: SocioServiceDep) -> Socio:
    socio = service.get_socio_by_id(socio_id)
    if not socio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Socio no encontrado"
        )
    return socio

@router.put("/{socio_id}", response_model=Socio)
def actualizar_socio(socio_id: int, socio_in: SocioUpdate, service: SocioServiceDep) -> Socio:
    try:
        socio = service.update_socio(socio_id, socio_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
        
    if not socio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Socio no encontrado"
        )
    return socio

@router.delete("/{socio_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_socio(socio_id: int, service: SocioServiceDep):
    success = service.delete_socio(socio_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Socio no encontrado"
        )
    return None

@router.get("/{socio_id}/prestamos", response_model=Sequence[Prestamo])
def listar_prestamos_de_socio(
    socio_id: int,
    prestamo_service: PrestamoServiceDep,
    activos: bool | None = None
) -> Sequence[Prestamo]:
    try:
        return prestamo_service.get_prestamos_por_socio(socio_id=socio_id, activos=activos)
    except LookupError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )