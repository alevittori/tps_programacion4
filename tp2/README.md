# Sistema de Gestión de Biblioteca (FastAPI + SQLModel)

API RESTful desarrollada en Python con **FastAPI** y **SQLModel** para la gestión integral del catálogo de una biblioteca, sus socios y el flujo de préstamos y devoluciones aplicando reglas de negocio y arquitectura en capas.

---

## Arquitectura y Estructura del Proyecto

El proyecto sigue una separación estricta de responsabilidades (Capas: **Routers → Services → Repositories → Models**):


tp2/
├── app/
│   ├── models/          # Modelos SQLModel (tablas y esquemas Create/Update/Response)
│   ├── repositories/    # Acceso a datos y consultas con SQLModel
│   ├── services/        # Lógica de negocio e interfaces (ABC) desacopladas de HTTP
│   ├── routers/         # Controladores y endpoints REST con manejo de errores HTTP
│   ├── database.py      # Configuración del motor SQLite y sesión de base de datos
│   ├── dependencies.py  # Inyección de dependencias centralizada con Annotated
│   └── main.py          # Punto de entrada de la aplicación FastAPI
├── test/               # Suite de pruebas automatizadas con pytest y base en memoria
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación del proyecto

# Requisitos Previos
    
    Python 3.11+

    Gestor de paquetes pip

# Instalación y Configuración

1 Clonar el repositorio:

    git clone [https://github.com/alevittori/tps_programacion4.git](https://github.com/alevittori/tps_programacion4.git)
    cd tps_programacion4

2 Crear y activar un entorno virtual:

En Windows (PowerShell / CMD):

    python -m venv .venv
    .venv\Scripts\activate

 En Linux / macOS:

    python3 -m venv .venv
    source .venv/bin/activate

3 Instalar las dependencias:

    pip install -r requirements.txt

# Cómo Ejecutar la Aplicación

Iniciá el servidor de desarrollo ejecutando:

    fastapi dev app/main.py

o si estas parado en tps_programacion4:

    fastapi dev tp2/app/main.py

(O alternativamente con Uvicorn: uvicorn app.main:app --reload)

Una vez iniciado el servidor, la API estará disponible en:

URL Base: http://127.0.0.1:8000

Documentación Interactiva (Swagger UI): http://127.0.0.1:8000/docs

Documentación Alternativa (ReDoc): http://127.0.0.1:8000/redoc

# Cómo Ejecutar los Tests y Verificar Cobertura
La suite de pruebas utiliza pytest junto con TestClient de FastAPI y una base de datos SQLite en memoria aislada por cada ejecución.

Ejecutar todos los tests:

    pytest -v

Ejecutar tests con reporte de cobertura:

    pytest --cov=app --cov-report=term-missing

    pytest --cov=tp2/app --cov-report=term-missing 

    (o pytest --cov=app --cov-report=term-missing si se ejecuta desde tp2/).


# Endpoints Principales

Autores (/autores)
    POST /autores/ — Registrar un nuevo autor (201 Created).

    GET /autores/ — Listar todos los autores (200 OK).

    GET /autores/{autor_id} — Obtener detalle de un autor (200 OK / 404 Not Found).

    PUT /autores/{autor_id} — Actualizar datos de un autor (200 OK).

    DELETE /autores/{autor_id} — Eliminar un autor (204 No Content).

Libros (/libros)
    POST /libros/ — Registrar un nuevo libro (201 Created / 409 Conflict si el ISBN ya existe).

    GET /libros/ — Listar libros. Admite el filtro opcional ?disponibles=true (stock > 0) o ?disponibles=false.

    GET /libros/{libro_id} — Obtener un libro por ID (200 OK / 404 Not Found).

    PUT /libros/{libro_id} — Actualizar datos o stock de un libro (200 OK).

    DELETE /libros/{libro_id} — Eliminar un libro (204 No Content).

    POST /libros/{libro_id}/autores/{autor_id} — Asociar un autor existente a un libro (relación N-N).

    DELETE /libros/{libro_id}/autores/{autor_id} — Desasociar un autor de un libro.

Socios (/socios)
    POST /socios/ — Registrar un nuevo socio (201 Created / 409 Conflict si el email ya existe).

    GET /socios/ — Listar todos los socios.

    GET /socios/{socio_id} — Obtener detalle de un socio (200 OK / 404 Not Found).

    PUT /socios/{socio_id} — Actualizar datos o estado (activo) de un socio.

    DELETE /socios/{socio_id} — Eliminar un socio (204 No Content).

    GET /socios/{socio_id}/prestamos — Listar historial de préstamos de un socio. Admite ?activos=true para filtrar los préstamos vigentes.

Préstamos (/prestamos)
    POST /prestamos/ — Registrar un nuevo préstamo (201 Created).

    POST /prestamos/{prestamo_id}/devolucion — Registrar la devolución de un libro (200 OK).

    GET /prestamos/ — Listar préstamos. Admite el filtro ?activos=true.

    GET /prestamos/{prestamo_id} — Obtener detalle de un préstamo.


# Reglas de Negocio Implementadas
Regla de Negocio   Código HTTP de Error

1 Un socio no puede tener más de 3 préstamos activos simultáneos.409 Conflict
2 No se presta un libro sin stock (stock == 0); al prestar se descuenta 1 unidad.409 Conflict
3 Un socio inactivo (activo == False) no puede solicitar préstamos.403 Forbidden
4 El plazo de préstamo es de 14 días (fecha_vencimiento = fecha_prestamo + 14 días).—
5 Al devolver se repone 1 unidad al stock y se calcula la multa: $100 × días de atraso ($0 si se devuelve en término).—
6 No se permite registrar la devolución de un préstamo ya devuelto.409 Conflict
7 Cualquier consulta u operación sobre un ID inexistente devuelve error.404 Not Found
8 No se permiten registros con ISBN o Email duplicados.409 Conflict