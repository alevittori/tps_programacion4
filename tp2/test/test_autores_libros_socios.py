def test_crud_autor_caso_feliz_y_404(client):
    # Crear autor (201)
    res = client.post("/autores/", json={"nombre": "Jorge Luis Borges", "nacionalidad": "Argentina"})
    assert res.status_code == 201
    autor_id = res.json()["id"]

    # Listar y obtener por ID (200)
    assert len(client.get("/autores/").json()) == 1
    assert client.get(f"/autores/{autor_id}").json()["nombre"] == "Jorge Luis Borges"

    # Actualizar (200)
    res_up = client.put(f"/autores/{autor_id}", json={"nombre": "J. L. Borges"})
    assert res_up.status_code == 200
    assert res_up.json()["nombre"] == "J. L. Borges"

    # Eliminar (204) y verificar 404 (Regla #7)
    assert client.delete(f"/autores/{autor_id}").status_code == 204
    assert client.get(f"/autores/{autor_id}").status_code == 404


def test_libros_regla_isbn_duplicado_y_filtro_disponibles(client):
    # Crear libro con stock > 0
    l1 = client.post("/libros/", json={
        "titulo": "Ficciones", "isbn": "978-01", "stock": 3, "anio": 1944
    })
    assert l1.status_code == 201

    # Regla #8 (Caso de error): ISBN duplicado -> 409 Conflict
    l_dup = client.post("/libros/", json={
        "titulo": "Otro libro", "isbn": "978-01", "stock": 1, "anio": 2000
    })
    assert l_dup.status_code == 409

    # Crear libro sin stock (stock = 0)
    l2 = client.post("/libros/", json={
        "titulo": "El Aleph", "isbn": "978-02", "stock": 0, "anio": 1949
    })
    assert l2.status_code == 201

    # Filtro GET /libros?disponibles=true (solo devuelve Ficciones)
    disponibles = client.get("/libros/?disponibles=true").json()
    assert len(disponibles) == 1
    assert disponibles[0]["titulo"] == "Ficciones"


def test_asociar_y_desasociar_autor_libro(client):
    autor_id = client.post("/autores/", json={"nombre": "Cortázar", "nacionalidad": "Argentina"}).json()["id"]
    libro_id = client.post("/libros/", json={"titulo": "Rayuela", "isbn": "978-03", "stock": 2, "anio": 1963}).json()["id"]

    # Asociar autor a libro (caso feliz)
    res_asoc = client.post(f"/libros/{libro_id}/autores/{autor_id}")
    assert res_asoc.status_code == 200

    # Asociar el mismo autor dos veces (caso de error -> 400)
    res_dup = client.post(f"/libros/{libro_id}/autores/{autor_id}")
    assert res_dup.status_code == 409

    # Desasociar autor (caso feliz)
    res_desasoc = client.delete(f"/libros/{libro_id}/autores/{autor_id}")
    assert res_desasoc.status_code == 200

    # Recurso inexistente -> 404 (Regla #7)
    assert client.post(f"/libros/999/autores/{autor_id}").status_code == 404


def test_socios_regla_email_duplicado(client):
    # Caso feliz
    s1 = client.post("/socios/", json={"nombre": "Ana Pérez", "email": "ana@test.com", "activo": True})
    assert s1.status_code == 201

    # Regla #8 (Caso de error): Email duplicado -> 409 Conflict
    s_dup = client.post("/socios/", json={"nombre": "Otra Ana", "email": "ana@test.com", "activo": True})
    assert s_dup.status_code == 409