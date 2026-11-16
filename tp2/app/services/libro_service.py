from abc import ABC, abstractmethod
from typing import Sequence
from app.models.libro import Libro, LibroCreate, LibroUpdate
from app.repositories.libro_repository import LibroRepositoryDep
from app.repositories.autor_repository import AutorRepositoryDep
from fastapi import HTTPException, status

class LibroServiceInterface(ABC):
    @abstractmethod
    def create_libro(self, libro_in: LibroCreate) -> Libro:
        ...

    @abstractmethod
    def get_libros(self, skip: int, limit: int) -> Sequence[Libro]:
        ...

    @abstractmethod
    def get_libro_by_id(self, libro_id: int) -> Libro | None:
        ...

    @abstractmethod
    def update_libro(self, libro_id: int, libro_in: LibroUpdate) -> Libro | None:
        ...

    @abstractmethod
    def delete_libro(self, libro_id: int) -> bool:
        ...
        
    @abstractmethod
    def asociar_autor(self, libro_id: int, autor_id: int) -> Libro:
        ...

    @abstractmethod
    def desasociar_autor(self, libro_id: int, autor_id: int) -> Libro:
        ...

class LibroService(LibroServiceInterface):
    def __init__(self, repo: LibroRepositoryDep, autor_repo: AutorRepositoryDep):
        self.repo = repo
        self.autor_repo = autor_repo

    def create_libro(self, libro_in: LibroCreate) -> Libro:
        # aca deberia agregar validaciones para que no se repitiera el isbn
        # Regla de negocio: Verificar si ya existe un libro con el mismo ISBN
        libro_existente = self.repo.get_by_isbn(libro_in.isbn)
        if libro_existente:
            raise ValueError(f"Ya existe un libro registrado con el ISBN '{libro_in.isbn}'.")
        return self.repo.create(libro_in)

    def get_libros(self, skip: int = 0, limit: int = 100) -> Sequence[Libro]:
        return self.repo.get_all(skip, limit)

    def get_libro_by_id(self, libro_id: int) -> Libro | None:
        return self.repo.get_by_id(libro_id)

    def update_libro(self, libro_id: int, libro_in: LibroUpdate) -> Libro | None:
        libro_db = self.repo.get_by_id(libro_id)
        if not libro_db:
            return None
        return self.repo.update(libro_db, libro_in)

    def delete_libro(self, libro_id: int) -> bool:
        libro_db = self.repo.get_by_id(libro_id)
        if not libro_db:
            return False
        self.repo.delete(libro_db)
        return True
    
    def asociar_autor(self, libro_id: int, autor_id: int) -> Libro:
        libro_db = self.repo.get_by_id(libro_id)
        if not libro_db:
            raise LookupError("Libro no encontrado")
            
        autor_db = self.autor_repo.get_by_id(autor_id)
        if not autor_db:
            raise LookupError("Autor no encontrado")

        # Regla de negocio: Evitar asociar el mismo autor dos veces al mismo libro
        if autor_db in libro_db.autores:
            raise ValueError("El autor ya se encuentra asociado a este libro.")

        return self.repo.add_autor(libro_db, autor_db)
    
    def desasociar_autor(self, libro_id: int, autor_id: int) -> Libro:
        libro_db = self.repo.get_by_id(libro_id)
        if not libro_db:
            raise LookupError("Libro no encontrado")

        autor_db = self.autor_repo.get_by_id(autor_id)
        if not autor_db:
            raise LookupError("Autor no encontrado")

        if autor_db not in libro_db.autores:
            raise ValueError("El autor no está asociado a este libro.")

        return self.repo.remove_autor(libro_db, autor_db)