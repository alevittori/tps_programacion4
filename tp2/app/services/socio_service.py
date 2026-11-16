from abc import ABC, abstractmethod
from typing import Sequence
from app.models.socio import Socio, SocioCreate, SocioUpdate
from app.repositories.socio_repository import SocioRepositoryDep

class SocioServiceInterface(ABC):
    @abstractmethod
    def create_socio(self, socio_in: SocioCreate) -> Socio:
        ...

    @abstractmethod
    def get_socios(self, skip: int, limit: int) -> Sequence[Socio]:
        ...

    @abstractmethod
    def get_socio_by_id(self, socio_id: int) -> Socio | None:
        ...

    @abstractmethod
    def update_socio(self, socio_id: int, socio_in: SocioUpdate) -> Socio | None:
        ...

    @abstractmethod
    def delete_socio(self, socio_id: int) -> bool:
        ...

class SocioService(SocioServiceInterface):
    def __init__(self, repo: SocioRepositoryDep):
        self.repo = repo

    def create_socio(self, socio_in: SocioCreate) -> Socio:
        # Regla de negocio: Email único
        socio_existente = self.repo.get_by_email(socio_in.email)
        if socio_existente:
            raise ValueError(f"Ya existe un socio registrado con el email '{socio_in.email}'.")
        
        return self.repo.create(socio_in)

    def get_socios(self, skip: int = 0, limit: int = 100) -> Sequence[Socio]:
        return self.repo.get_all(skip, limit)

    def get_socio_by_id(self, socio_id: int) -> Socio | None:
        return self.repo.get_by_id(socio_id)

    def update_socio(self, socio_id: int, socio_in: SocioUpdate) -> Socio | None:
        socio_db = self.repo.get_by_id(socio_id)
        if not socio_db:
            return None

        # Regla de negocio: Validar que el nuevo email no pertenezca a otro socio
        if socio_in.email and socio_in.email != socio_db.email:
            email_existente = self.repo.get_by_email(socio_in.email)
            if email_existente:
                raise ValueError(f"El email '{socio_in.email}' ya está en uso por otro socio.")

        return self.repo.update(socio_db, socio_in)

    def delete_socio(self, socio_id: int) -> bool:
        socio_db = self.repo.get_by_id(socio_id)
        if not socio_db:
            return False
        self.repo.delete(socio_db)
        return True