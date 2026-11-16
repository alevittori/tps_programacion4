from abc import ABC, abstractmethod
from typing import Sequence
from datetime import date, timedelta
from app.models.prestamo import Prestamo, PrestamoCreate,PrestamoUpdate
from app.repositories.prestamo_repository import PrestamoRepositoryDep
from app.repositories.libro_repository import LibroRepositoryDep
from app.repositories.socio_repository import SocioRepositoryDep

# Constantes de negocio
MAX_PRESTAMOS_ACTIVOS = 3
DIAS_PLAZO_PRESTAMO = 14
MONTO_MULTA_POR_DIA = 500.0

class PrestamoServiceInterface(ABC):
    @abstractmethod
    def registrar_prestamo(self, prestamo_in: PrestamoCreate) -> Prestamo:
        ...

    @abstractmethod
    def registrar_devolucion(self, prestamo_id: int) -> Prestamo:
        ...

    @abstractmethod
    def get_prestamos(self, skip: int, limit: int, activos: bool | None) -> Sequence[Prestamo]:
        ...

    @abstractmethod
    def get_prestamo_by_id(self, prestamo_id: int) -> Prestamo | None:
        ...

   
    @abstractmethod
    def get_prestamos_por_socio(self, socio_id: int, activos: bool | None = None) -> Sequence[Prestamo]:
        ...

class PrestamoService(PrestamoServiceInterface):
    def __init__(
        self,
        repo: PrestamoRepositoryDep,
        libro_repo: LibroRepositoryDep,
        socio_repo: SocioRepositoryDep
    ):
        self.repo = repo
        self.libro_repo = libro_repo
        self.socio_repo = socio_repo

    def registrar_prestamo(self, prestamo_in: PrestamoCreate) -> Prestamo:
        #  Validar que el socio exista
        socio = self.socio_repo.get_by_id(prestamo_in.socio_id)
        if not socio:
            raise LookupError("Socio no encontrado.")

        #  Validar que el socio esté activo
        if not socio.activo:
            raise ValueError("El socio se encuentra inactivo y no puede solicitar préstamos.")

        #  Validar que el libro exista
        libro = self.libro_repo.get_by_id(prestamo_in.libro_id)
        if not libro:
            raise LookupError("Libro no encontrado.")

        #  Validar que haya stock disponible
        if libro.stock <= 0:
            raise ValueError(f"No hay stock disponible para el libro '{libro.titulo}'.")

        #  Validar el límite máximo de 3 préstamos activos por socio
        prestamos_activos = self.repo.count_activos_by_socio(socio.id)
        if prestamos_activos >= MAX_PRESTAMOS_ACTIVOS:
            raise ValueError(f"El socio ya alcanzó el límite máximo de {MAX_PRESTAMOS_ACTIVOS} préstamos activos.")

        #  Calcular fechas por regla de negocio y armar el objeto Prestamo
        hoy = date.today()
        nuevo_prestamo = Prestamo(
            socio_id=prestamo_in.socio_id,
            libro_id=prestamo_in.libro_id,
            fecha_prestamo=hoy,
            fecha_vencimiento=hoy + timedelta(days=DIAS_PLAZO_PRESTAMO),
            multa=0.0
        )

        #  Descontar 1 unidad del stock del libro
        libro.stock -= 1
        self.libro_repo.session.add(libro)

        # Guardar el préstamo (el commit confirma también la baja de stock en la misma sesión)
        return self.repo.create(nuevo_prestamo)

    def registrar_devolucion(self, prestamo_id: int) -> Prestamo:
        #  Buscar el préstamo
        prestamo = self.repo.get_by_id(prestamo_id)
        if not prestamo:
            raise LookupError("Préstamo no encontrado.")

        #  Verificar que no haya sido devuelto previamente
        if prestamo.fecha_devolucion is not None:
            raise ValueError("Este préstamo ya fue devuelto anteriormente.")

        #  Registrar fecha de devolución actual
        hoy = date.today()
        prestamo.fecha_devolucion = hoy

        #  Calcular multa si corresponde (si devolvió después de la fecha de vencimiento)
        if hoy > prestamo.fecha_vencimiento:
            dias_retraso = (hoy - prestamo.fecha_vencimiento).days
            prestamo.multa = dias_retraso * MONTO_MULTA_POR_DIA

        #  Reponer 1 unidad al stock del libro
        libro = self.libro_repo.get_by_id(prestamo.libro_id)
        if libro:
            libro.stock += 1
            self.libro_repo.session.add(libro)

        return self.repo.update(prestamo)

    def get_prestamos(self, skip: int = 0, limit: int = 100, activos: bool | None = None) -> Sequence[Prestamo]:
        return self.repo.get_all(skip, limit, activos)

    def get_prestamo_by_id(self, prestamo_id: int) -> Prestamo | None:
        return self.repo.get_by_id(prestamo_id)

    def get_prestamos_por_socio(self, socio_id: int, activos: bool | None = None) -> Sequence[Prestamo]:
        socio = self.socio_repo.get_by_id(socio_id)
        if not socio:
            raise LookupError("Socio no encontrado.")
        return self.repo.get_by_socio(socio_id, activos=activos)
    
    
    # Funcion por si queremos actualizar manualmente la devolucion
    def actualizar_prestamo(self, prestamo_id: int, prestamo_in: PrestamoUpdate) -> Prestamo | None:
     prestamo = self.repo.get_by_id(prestamo_id)
     if not prestamo:
        return None

        # Si se carga una fecha de devolución manual, recalculamos la multa
     if prestamo_in.fecha_devolucion is not None:
        prestamo.fecha_devolucion = prestamo_in.fecha_devolucion
        if prestamo.fecha_devolucion > prestamo.fecha_vencimiento:
            dias_retraso = (prestamo.fecha_devolucion - prestamo.fecha_vencimiento).days
            prestamo.multa = dias_retraso * MONTO_MULTA_POR_DIA
        else:
            prestamo.multa = 0.0

     if prestamo_in.multa is not None:
        prestamo.multa = prestamo_in.multa

     return self.repo.update(prestamo)