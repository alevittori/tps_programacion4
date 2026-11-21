from typing import Sequence
from fastapi import APIRouter, HTTPException, status
from app.dependencies import PrestamoServiceDep
from app.models.prestamo import Prestamo, PrestamoCreate,PrestamoUpdate

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])


@router.post("/", response_model=Prestamo, status_code=status.HTTP_201_CREATED)
def crear_prestamo(prestamo_in: PrestamoCreate, service: PrestamoServiceDep) -> Prestamo:
    try:
        return service.registrar_prestamo(prestamo_in)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/{prestamo_id}/devolucion", response_model=Prestamo)
def devolver_prestamo(prestamo_id: int, service: PrestamoServiceDep) -> Prestamo:
    try:
        return service.registrar_devolucion(prestamo_id)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
@router.get("/", response_model=Sequence[Prestamo])
def listar_prestamos(
    service: PrestamoServiceDep,
    activos: bool | None = None,
    skip: int = 0,
    limit: int = 100
) -> Sequence[Prestamo]:
    return service.get_prestamos(skip=skip, limit=limit, activos=activos)

@router.get("/{prestamo_id}", response_model=Prestamo)
def obtener_prestamo(prestamo_id: int, service: PrestamoServiceDep) -> Prestamo:
    prestamo = service.get_prestamo_by_id(prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo no encontrado")
    return prestamo

@router.get("/socio/{socio_id}", response_model=Sequence[Prestamo])
def listar_prestamos_socio(socio_id: int, service: PrestamoServiceDep) -> Sequence[Prestamo]:
    try:
        return service.get_prestamos_por_socio(socio_id)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    
#Para mandar una devolucion manual, sin esperar los 14 dias
@router.patch("/{prestamo_id}", response_model=Prestamo)
def actualizar_prestamo(prestamo_id: int, prestamo_in: PrestamoUpdate, service: PrestamoServiceDep) -> Prestamo:
    prestamo = service.actualizar_prestamo(prestamo_id, prestamo_in)
    if not prestamo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo no encontrado")
    return prestamo