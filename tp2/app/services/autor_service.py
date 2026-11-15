from abc import ABC, abstractmethod
from typing import Sequence
from app.models.autor import Autor, AutorCreate, AutorUpdate
from app.repositories.autor_repository import AutorRepositoryDep

class AutorServiceInterface(ABC):
    @abstractmethod
    def create_autor(self, autor_in: AutorCreate) -> Autor:
        ...

    @abstractmethod
    def get_autores(self, skip: int, limit: int) -> Sequence[Autor]:
        ...

    @abstractmethod
    def get_autor_by_id(self, autor_id: int) -> Autor | None:
        ...

    @abstractmethod
    def update_autor(self, autor_id: int, autor_in: AutorUpdate) -> Autor | None:
        ...

    @abstractmethod
    def delete_autor(self, autor_id: int) -> bool:
        ...

class AutorService(AutorServiceInterface):
    def __init__(self, repo: AutorRepositoryDep):
        self.repo = repo

    def create_autor(self, autor_in: AutorCreate) -> Autor:
        return self.repo.create(autor_in)

    def get_autores(self, skip: int = 0, limit: int = 100) -> Sequence[Autor]:
        return self.repo.get_all(skip, limit)

    def get_autor_by_id(self, autor_id: int) -> Autor | None:
        return self.repo.get_by_id(autor_id)

    def update_autor(self, autor_id: int, autor_in: AutorUpdate) -> Autor | None:
        autor_db = self.repo.get_by_id(autor_id)
        if not autor_db:
            return None
        return self.repo.update(autor_db, autor_in)

    def delete_autor(self, autor_id: int) -> bool:
        autor_db = self.repo.get_by_id(autor_id)
        if not autor_db:
            return False
        self.repo.delete(autor_db)
        return True