from typing import Annotated
from fastapi import Depends


from app.services.autor_service import AutorService, AutorServiceInterface





# Dependencias de Servicios (usando la interfaz ABC)
AutorServiceDep = Annotated[AutorServiceInterface, Depends(AutorService)]