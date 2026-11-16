from typing import Annotated, Sequence
from fastapi import Depends
from sqlmodel import select
from app.database import SessionDep
from app.models.socio import Socio, SocioCreate, SocioUpdate

class SocioRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def create(self, socio_in: SocioCreate) -> Socio:
        socio = Socio.model_validate(socio_in)
        self.session.add(socio)
        self.session.commit()
        self.session.refresh(socio)
        return socio

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Socio]:
        statement = select(Socio).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_by_id(self, socio_id: int) -> Socio | None:
        return self.session.get(Socio, socio_id)

    def get_by_email(self, email: str) -> Socio | None:
        statement = select(Socio).where(Socio.email == email)
        return self.session.exec(statement).first()

    def update(self, socio_db: Socio, socio_in: SocioUpdate) -> Socio:
        socio_data = socio_in.model_dump(exclude_unset=True)
        for key, value in socio_data.items():
            setattr(socio_db, key, value)
        self.session.add(socio_db)
        self.session.commit()
        self.session.refresh(socio_db)
        return socio_db

    def delete(self, socio_db: Socio) -> None:
        self.session.delete(socio_db)
        self.session.commit()

SocioRepositoryDep = Annotated[SocioRepository, Depends(SocioRepository)]
