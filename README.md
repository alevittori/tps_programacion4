# tps_programacion4
repo para los tp de programacion 4 utn

Trabajo Práctico: ABM de Usuarios con FastAPI + ABM propio
Objetivo
Completar y extender la API de ejemplo vista en clase (clase-fastapi) para tener un ABM (Alta, Baja, Modificación) completo de usuarios, y luego replicar ese mismo patrón para crear el ABM de una entidad propia.

Parte 1 — Completar el ABM de usuarios
Sobre el proyecto clase-fastapi (el que se armó en clase), agregar/completar los siguientes endpoints sobre la entidad Usuario:

Eliminar un usuario por id (DELETE).
Modificar los datos de un usuario existente (PUT o PATCH).
Buscar/listar usuarios filtrando por estado: activos, inactivos, o todos (por ejemplo vía un query param is_active).
Los endpoints ya existentes de alta y listado se pueden mantener o mejorar, pero el foco de esta parte es completar lo que falta.

Parte 2 — ABM de una entidad propia
Elegir una entidad distinta a Usuario, con 5 campos, y construir un ABM/CRUD completo (crear, listar, obtener por id, modificar, eliminar y buscar/filtrar por algún campo relevante), siguiendo el mismo patrón usado para usuarios (modelos con Pydantic, router de FastAPI, almacenamiento en memoria).

Por ejemplo, la entiedad "Auto" con id, marca, modelo, número de chasis y año.

IMPORTANTE: No usar la entidad Auto dada de ejemplo.

Entrega
Un link a un repositorio (GitHub o similar) con el código de la aplicación funcionando.
Un README.md con instrucciones claras de cómo:
Instalar dependencias y levantar la aplicación.
Acceder a la documentación interactiva (Swagger) en /docs para poder probar todos los endpoints.
Plazo
La entrega debe realizarse antes de finalizar el cuatrimestre, para poder obtener la regularidad de la materia.

**************************************


TP: Sistema de Biblioteca (FastAPI + SQLModel)
Objetivo
Construir una API REST para gestionar el catálogo de una biblioteca y sus préstamos. Hay que modelar entidades con relaciones y aplicar reglas de negocio con los códigos HTTP correctos.

Modelo de datos
Entidad	Campos
Autor	id, nombre, nacionalidad
Libro	id, titulo, isbn (único), stock (≥ 0), anio
LibroAutor	libro_id, autor_id (tabla intermedia)
Socio	id, nombre, email (único), activo
Prestamo	id, socio_id, libro_id, fecha_prestamo, fecha_vencimiento, fecha_devolucion (nullable), multa
Relaciones:

Libro N-N Autor.
Préstamo N-1 Socio.
Préstamo N-1 Libro.
Endpoints mínimos
Método	Ruta	Descripción
CRUD	/autores, /libros, /socios	Alta, baja, modificación y consulta
POST	/libros/{id}/autores/{autor_id}	Asocia un autor a un libro
GET	/libros?disponibles=true	Libros con stock > 0
POST	/prestamos	Registra un préstamo
POST	/prestamos/{id}/devolucion	Registra la devolución
GET	/socios/{id}/prestamos?activos=true	Préstamos activos del socio
Reglas de negocio
#	Regla	Error
1	Un socio no puede tener más de 3 préstamos activos	409
2	No se presta un libro sin stock; al prestar se descuenta 1	409
3	Un socio inactivo no puede pedir préstamos	403
4	El plazo es de 14 días; fecha_vencimiento = fecha_prestamo + 14 días	n/a
5	Al devolver se repone el stock y se calcula la multa: $100 × días de atraso (0 si llegó a tiempo)	n/a
6	No se puede devolver un préstamo ya devuelto	409
7	Recurso inexistente	404
8	ISBN o email duplicado	409
Etapas sugeridas
CRUD y modelos: SQLModel, sesión de base de datos, routers por entidad.
Relaciones: N-N Libro/Autor y respuestas que incluyan los autores del libro.
Préstamos: reglas de negocio en una capa services, no en el router.
Tests: pytest con base en memoria, cobertura ≥ 80 %.
Opcional: roles bibliotecario y socio. Solo el bibliotecario administra el catálogo, y el socio ve únicamente sus préstamos.
Entrega
Repositorio con README (cómo correr y cómo testear).
Estructura sugerida: models/, routers/, services/, tests/.
Tests que cubran cada regla de negocio, tanto el caso feliz como el de error.
Rúbrica (100 pts)
Criterio	Pts
Modelo y relaciones correctas	20
Endpoints y códigos HTTP	20
Reglas de negocio	25
Tests y cobertura	20
Estructura y claridad del código	15