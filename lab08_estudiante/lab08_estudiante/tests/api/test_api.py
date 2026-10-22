"""NIVEL DE INTEGRACIÓN (API) — Playwright APIRequestContext.

Objeto de prueba: el contrato HTTP de /api/... (rutas, códigos de estado, JSON).
Fixtures disponibles (ver tests/conftest.py):
    api               -> cliente sin token
    api_autenticada   -> cliente con token válido
Los datos se reinician antes de cada prueba (3 productos iniciales, ids 1, 2 y 3).

Ejecuta solo este nivel:   pytest tests/api -v
"""


"""NIVEL DE INTEGRACIÓN (API) — Playwright APIRequestContext."""


# ---------------------------------------------------------------- EJEMPLO
def test_listar_productos_devuelve_los_tres_iniciales(api_autenticada):
    respuesta = api_autenticada.get("/api/productos")
    assert respuesta.status == 200
    assert len(respuesta.json()) == 3


# ---------------------------------------------------------------- LOGIN
def test_login_correcto_devuelve_token(api):
    r = api.post("/api/login", data={"usuario": "admin", "password": "Admin123"})
    assert r.status == 200
    assert "token" in r.json()


def test_login_incorrecto_devuelve_401(api):
    r = api.post("/api/login", data={"usuario": "admin", "password": "wrongpass"})
    assert r.status == 401


def test_login_formato_invalido_devuelve_400(api):
    r = api.post("/api/login", data={"usuario": "", "password": "123"})
    assert r.status == 400
    assert "errores" in r.json()


# ---------------------------------------------------------------- SEGURIDAD
def test_sin_token_devuelve_401(api):
    r = api.get("/api/productos")
    assert r.status == 401


# ---------------------------------------------------------------- CRUD
def test_crear_producto_valido_devuelve_201(api_autenticada):
    r = api_autenticada.post("/api/productos",
                             data={"nombre": "Audífonos", "precio": 199.99, "stock": 3})
    assert r.status == 201
    assert r.json()["id"] is not None


def test_obtener_producto_existente_devuelve_200(api_autenticada):
    r = api_autenticada.get("/api/productos/1")
    assert r.status == 200
    assert r.json()["nombre"] == "Teclado"


def test_actualizar_producto_devuelve_200(api_autenticada):
    r = api_autenticada.put("/api/productos/1",
                            data={"nombre": "Teclado Mecánico", "precio": 350.0, "stock": 8})
    assert r.status == 200
    assert r.json()["nombre"] == "Teclado Mecánico"


def test_eliminar_producto_existente_devuelve_204(api_autenticada):
    r = api_autenticada.delete("/api/productos/1")
    assert r.status == 204


# ---------------------------------------------------------------- NEGATIVOS
def test_crear_producto_invalido_devuelve_400(api_autenticada):
    r = api_autenticada.post("/api/productos",
                             data={"nombre": "ab", "precio": 0, "stock": -1})
    assert r.status == 400
    assert "errores" in r.json()


def test_obtener_producto_inexistente_devuelve_404(api_autenticada):
    r = api_autenticada.get("/api/productos/999")
    assert r.status == 404


def test_actualizar_producto_inexistente_devuelve_404(api_autenticada):
    r = api_autenticada.put("/api/productos/999",
                            data={"nombre": "Fantasma", "precio": 10.0, "stock": 1})
    assert r.status == 404


def test_eliminar_producto_inexistente_devuelve_404(api_autenticada):
    r = api_autenticada.delete("/api/productos/999")
    assert r.status == 404




# ------------------------------------------------------------------ TODO
# Usa la tabla "Contrato de la API" de la guía como ORÁCULO.
# 1. Login: credenciales correctas (200 + token) e incorrectas (401).
# 2. Seguridad mínima: sin token -> 401.
# 3. CRUD: crear (201), consultar, actualizar y eliminar (204).
# 4. Casos negativos: datos inválidos (400) y recursos que NO existen.
#    Verifica el código de estado exacto que exige el contrato.
#
# Ejemplo de POST con JSON:
#     r = api_autenticada.post("/api/productos",
#                              data={"nombre": "Audífonos", "precio": 199.99, "stock": 3})
#     assert r.status == 201
