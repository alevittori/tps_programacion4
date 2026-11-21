from datetime import date, timedelta


def _crear_socio(client, email="socio@test.com", activo=True):
    return client.post("/socios/", json={"nombre": "Juan", "email": email, "activo": activo}).json()


def _crear_libro(client, isbn="111-222", stock=5):
    return client.post("/libros/", json={"titulo": "Clean Code", "isbn": isbn, "stock": stock, "anio": 2008}).json()


def test_prestamo_caso_feliz_plazo_y_stock(client):
    socio = _crear_socio(client)
    libro = _crear_libro(client, stock=3)

    # Registrar préstamo (201)
    res = client.post("/prestamos/", json={"socio_id": socio["id"], "libro_id": libro["id"]})
    assert res.status_code == 201
    data = res.json()

    # Regla #4: Plazo de 14 días exactos
    hoy = date.today()
    assert data["fecha_prestamo"] == str(hoy)
    assert data["fecha_vencimiento"] == str(hoy + timedelta(days=14))
    assert data["fecha_devolucion"] is None
    assert data["multa"] == 0.0

    # Regla #2: Stock descontado en 1 (3 -> 2)
    libro_actualizado = client.get(f"/libros/{libro['id']}").json()
    assert libro_actualizado["stock"] == 2

    # Endpoint GET /socios/{id}/prestamos?activos=true
    activos = client.get(f"/socios/{socio['id']}/prestamos?activos=true").json()
    assert len(activos) == 1


def test_regla_1_maximo_3_prestamos_activos(client):
    socio = _crear_socio(client)
    libro = _crear_libro(client, stock=10)

    # Crear 3 préstamos activos (deben pasar todos)
    for _ in range(3):
        res = client.post("/prestamos/", json={"socio_id": socio["id"], "libro_id": libro["id"]})
        assert res.status_code == 201

    # Intentar un 4to préstamo activo -> 409 Conflict
    res_4to = client.post("/prestamos/", json={"socio_id": socio["id"], "libro_id": libro["id"]})
    assert res_4to.status_code == 409


def test_regla_2_libro_sin_stock(client):
    socio = _crear_socio(client)
    libro = _crear_libro(client, stock=0)

    # Intentar prestar libro con stock 0 -> 409 Conflict
    res = client.post("/prestamos/", json={"socio_id": socio["id"], "libro_id": libro["id"]})
    assert res.status_code == 409


def test_regla_3_socio_inactivo(client):
    socio = _crear_socio(client, activo=False)
    libro = _crear_libro(client, stock=5)

    # Socio inactivo -> 403 Forbidden
    res = client.post("/prestamos/", json={"socio_id": socio["id"], "libro_id": libro["id"]})
    assert res.status_code == 403


def test_regla_5_y_6_devolucion_reposicion_stock_multa_y_doble_devolucion(client):
    socio = _crear_socio(client)
    libro = _crear_libro(client, stock=2)

    prestamo = client.post("/prestamos/", json={"socio_id": socio["id"], "libro_id": libro["id"]}).json()
    prestamo_id = prestamo["id"]

    # Devolución en término (Regla #5: repone stock 1 -> 2, multa = 0)
    res_dev = client.post(f"/prestamos/{prestamo_id}/devolucion")
    assert res_dev.status_code == 200
    assert res_dev.json()["multa"] == 0.0
    assert client.get(f"/libros/{libro['id']}").json()["stock"] == 2

    # Regla #6: Intentar devolver un préstamo ya devuelto -> 409 Conflict
    res_doble = client.post(f"/prestamos/{prestamo_id}/devolucion")
    assert res_doble.status_code == 409


def test_regla_5_calculo_multa_por_atraso(client):
    socio = _crear_socio(client)
    libro = _crear_libro(client, stock=2)

    prestamo = client.post("/prestamos/", json={"socio_id": socio["id"], "libro_id": libro["id"]}).json()
    prestamo_id = prestamo["id"]

    # Simulamos devolución 3 días después del vencimiento ($100 x 3 = $300)
    fecha_atrasada = date.today() + timedelta(days=17)
    res_patch = client.patch(f"/prestamos/{prestamo_id}", json={"fecha_devolucion": str(fecha_atrasada)})
    assert res_patch.status_code == 200
    assert res_patch.json()["multa"] == 300.0


def test_regla_7_recursos_inexistentes_404(client):
    socio = _crear_socio(client)
    libro = _crear_libro(client)

    assert client.post("/prestamos/", json={"socio_id": 999, "libro_id": libro["id"]}).status_code == 404
    assert client.post("/prestamos/", json={"socio_id": socio["id"], "libro_id": 999}).status_code == 404
    assert client.post("/prestamos/999/devolucion").status_code == 404
    assert client.get("/socios/999/prestamos").status_code == 404