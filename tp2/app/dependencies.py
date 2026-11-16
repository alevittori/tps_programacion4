from typing import Annotated
from fastapi import Depends


from app.services.autor_service import AutorService, AutorServiceInterface
from app.services.libro_service import LibroService, LibroServiceInterface
from app.services.socio_service import SocioService, SocioServiceInterface
from app.services.prestamo_service import PrestamoService, PrestamoServiceInterface




# Dependencias de Servicios 
AutorServiceDep = Annotated[AutorServiceInterface, Depends(AutorService)]
LibroServiceDep = Annotated[LibroServiceInterface, Depends(LibroService)]
SocioServiceDep = Annotated[SocioServiceInterface, Depends(SocioService)]
PrestamoServiceDep = Annotated[PrestamoServiceInterface, Depends(PrestamoService)]