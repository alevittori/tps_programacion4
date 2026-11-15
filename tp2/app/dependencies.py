from typing import Annotated
from fastapi import Depends


from app.services.autor_service import AutorService, AutorServiceInterface
from app.services.libro_service import LibroService, LibroServiceInterface





# Dependencias de Servicios 
AutorServiceDep = Annotated[AutorServiceInterface, Depends(AutorService)]
LibroServiceDep = Annotated[LibroServiceInterface, Depends(LibroService)]