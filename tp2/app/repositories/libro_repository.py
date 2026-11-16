from typing import Annotated, Sequence
from fastapi import Depends
from sqlmodel import select
from app.database import  SessionDep

from app.models.libro import Libro,LibroCreate,LibroUpdate,LibroAutorLink
from app.models.autor import Autor

class LibroRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def create(self, libro_in: LibroCreate) -> Libro:
        libro = Libro.model_validate(libro_in)
        self.session.add(libro)
        self.session.commit()
        self.session.refresh(libro)
        return libro

 
    def get_all(self, skip: int = 0, limit: int = 100, disponibles: bool | None = None) -> Sequence[Libro]:
        statement = select(Libro)
        
        # Filtro opcional por disponibilidad de stock
        if disponibles is True:
            statement = statement.where(Libro.stock > 0)
        elif disponibles is False:
            statement = statement.where(Libro.stock == 0)
            
        statement = statement.offset(skip).limit(limit)
        return self.session.exec(statement).all()
    
    
    def get_by_id(self, libro_id: int) -> Libro | None:
        return self.session.get(Libro, libro_id)

    def get_by_isbn(self, isbn: str) -> Libro | None:
        statement = select(Libro).where(Libro.isbn == isbn)
        return self.session.exec(statement).first()

    def update(self, libro_db: Libro, libro_in: LibroUpdate) -> Libro:
        libro_data = libro_in.model_dump(exclude_unset=True)
        for key, value in libro_data.items():
            setattr(libro_db, key, value)
        self.session.add(libro_db)
        self.session.commit()
        self.session.refresh(libro_db)
        return libro_db

    def delete(self, libro_db: Libro) -> None:
        self.session.delete(libro_db)
        self.session.commit()
         
    
            
    def add_autor(self, libro_db: Libro, autor_db: Autor) -> Libro:
        """Asocia un autor a un libro usando la relación N-N de SQLModel."""
        libro_db.autores.append(autor_db)
        self.session.add(libro_db)
        self.session.commit()
        self.session.refresh(libro_db)
        return libro_db
    
    
LibroRepositoryDep = Annotated[LibroRepository, Depends(LibroRepository)]