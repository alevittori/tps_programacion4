from typing import Annotated, Sequence
from fastapi import Depends
from sqlmodel import select
#from app.dependencies import SessionDep
from app.database import  SessionDep
from app.models.autor import Autor, AutorCreate, AutorUpdate

class AutorRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def create(self, autor_in: AutorCreate) -> Autor:
        autor = Autor.model_validate(autor_in)
        self.session.add(autor)
        self.session.commit()
        self.session.refresh(autor)
        return autor

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Autor]:
        statement = select(Autor).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_by_id(self, autor_id: int) -> Autor | None:
        return self.session.get(Autor, autor_id)

    def update(self, autor_db: Autor, autor_in: AutorUpdate) -> Autor:
        autor_data = autor_in.model_dump(exclude_unset=True)
        for key, value in autor_data.items():
            setattr(autor_db, key, value)
        self.session.add(autor_db)
        self.session.commit()
        self.session.refresh(autor_db)
        return autor_db

    def delete(self, autor_db: Autor) -> None:
        self.session.delete(autor_db)
        self.session.commit()
        
        
AutorRepositoryDep = Annotated[AutorRepository, Depends(AutorRepository)]