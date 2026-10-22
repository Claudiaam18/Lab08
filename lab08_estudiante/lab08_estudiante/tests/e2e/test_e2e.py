"""NIVEL DE SISTEMA (E2E) — Playwright en un navegador real.

Objeto de prueba: los flujos del usuario en la interfaz web.
La fixture `page` la provee pytest-playwright; las rutas relativas usan base_url.
Los datos se reinician antes de cada prueba.

Ejecuta solo este nivel:          pytest tests/e2e -v
Para VER el navegador:            pytest tests/e2e --headed --slowmo 500
Para grabar interacciones:        playwright codegen http://127.0.0.1:5000
                                  (con la app corriendo: python run.py)
"""
from playwright.sync_api import Page, expect


# ---------------------------------------------------------------- EJEMPLO
def test_pagina_de_login_carga(page: Page):
    page.goto("/login")
    expect(page.get_by_role("heading", name="Iniciar sesión")).to_be_visible()

# helper para no repetir el flujo de login
def _login(page, usuario="admin", password="Admin123"):
    page.goto("/login")
    page.get_by_label("Usuario").fill(usuario)
    page.get_by_label("Contraseña").fill(password)
    page.get_by_role("button", name="Ingresar").click()


def test_login_exitoso_muestra_bienvenida(page: Page):
    _login(page)
    # "Bienvenido, admin" aparece con 800 ms de retraso — expect() espera solo
    expect(page.get_by_text("Bienvenido, admin")).to_be_visible()


def test_login_fallido_muestra_error(page: Page):
    _login(page, password="incorrecta")
    expect(page.get_by_text("Usuario o contraseña incorrectos")).to_be_visible()


def test_crear_producto_aparece_en_tabla(page: Page):
    _login(page)
    page.get_by_role("link", name="Nuevo producto").click()
    page.get_by_label("Nombre").fill("Audífonos")
    page.get_by_label("Precio").fill("199.99")
    page.get_by_label("Stock").fill("3")
    page.get_by_role("button", name="Guardar").click()
    expect(page.get_by_text("Producto creado")).to_be_visible()
    expect(page.get_by_role("cell", name="Audífonos")).to_be_visible()


def test_eliminar_producto_no_afecta_los_demas(page: Page):
    _login(page)
    # Intenta eliminar el Mouse (id=2), NO el primero
    fila = page.get_by_role("row").filter(has_text="Mouse")
    fila.get_by_role("button", name="Eliminar").click()
    expect(page.get_by_text("Producto eliminado")).to_be_visible()
    # Mouse debe haber desaparecido
    expect(page.get_by_role("cell", name="Mouse")).not_to_be_visible()
    # Teclado (id=1) no debería verse afectado — AQUÍ FALLA si hay defecto
    expect(page.get_by_role("cell", name="Teclado")).to_be_visible()


# ------------------------------------------------------------------ TODO
# 1. Login exitoso: debe mostrarse "Bienvenido, admin".
def test_inicio_exitoso(page: Page) -> None:
    page.goto("http://127.0.0.1:5000/login")
    page.get_by_role("textbox", name="Usuario").click()
    page.get_by_role("textbox", name="Usuario").fill("admin")
    page.get_by_role("textbox", name="Contraseña").click()
    page.get_by_role("textbox", name="Contraseña").click()
    page.get_by_role("textbox", name="Contraseña").fill("Admin123")
    page.get_by_role("textbox", name="Contraseña").press("Enter")

#    (Ojo: aparece con retraso. NO uses time.sleep: expect() espera solo.)
# 2. Login fallido: se muestra un mensaje de error.
def test_example(page: Page) -> None:
    page.goto("http://127.0.0.1:5000/login")
    page.get_by_role("textbox", name="Usuario").click()
    page.get_by_role("textbox", name="Usuario").fill("admin")
    page.get_by_role("textbox", name="Contraseña").click()
    page.get_by_role("textbox", name="Contraseña").click()
    page.get_by_role("textbox", name="Contraseña").fill("Admin123")
    page.get_by_role("textbox", name="Contraseña").press("Enter")
    page.get_by_role("link", name="Cerrar sesión").click()
    page.get_by_role("textbox", name="Usuario").click()
    page.get_by_role("textbox", name="Usuario").fill("admin")
    page.get_by_role("textbox", name="Usuario").press("Tab")
    page.get_by_role("textbox", name="Contraseña").fill("admin")
    page.get_by_role("textbox", name="Contraseña").press("Enter")
# 3. Crear un producto desde el formulario y verificar que aparece en la tabla.
def test_example(page: Page) -> None:
    page.goto("http://127.0.0.1:5000/login")
    page.get_by_role("textbox", name="Usuario").click()
    page.get_by_role("textbox", name="Usuario").fill("admin")
    page.get_by_role("textbox", name="Contraseña").click()
    page.get_by_role("textbox", name="Contraseña").click()
    page.get_by_role("textbox", name="Contraseña").fill("Admin123")
    page.get_by_role("textbox", name="Contraseña").press("Enter")
    page.get_by_role("link", name="Cerrar sesión").click()
    page.get_by_role("textbox", name="Usuario").click()
    page.get_by_role("textbox", name="Usuario").fill("admin")
    page.get_by_role("textbox", name="Usuario").press("Tab")
    page.get_by_role("textbox", name="Contraseña").fill("admin")
    page.get_by_role("textbox", name="Contraseña").press("Enter")
    page.get_by_role("textbox", name="Usuario").click()
    page.get_by_role("textbox", name="Usuario").fill("admin")
    page.get_by_role("textbox", name="Usuario").press("Tab")
    page.get_by_role("textbox", name="Contraseña").fill("Admin123")
    page.get_by_role("textbox", name="Contraseña").press("Enter")
    page.get_by_role("link", name="Nuevo producto").click()
    page.get_by_role("textbox", name="Nombre").click()
    page.get_by_role("textbox", name="Nombre").press("CapsLock")
    page.get_by_role("textbox", name="Nombre").fill("M")
    page.get_by_role("textbox", name="Nombre").press("CapsLock")
    page.get_by_role("textbox", name="Nombre").fill("Mousepad")
    page.get_by_role("textbox", name="Nombre").press("Tab")
    page.get_by_role("textbox", name="Precio").fill("20")
    page.get_by_role("textbox", name="Precio").press("Tab")
    page.get_by_role("textbox", name="Stock").fill("10")
    page.get_by_role("button", name="Guardar").click()
# 4. Eliminar un producto desde la tabla.
def test_example(page: Page) -> None:
    page.goto("http://127.0.0.1:5000/login")
    page.get_by_role("textbox", name="Usuario").click()
    page.get_by_role("textbox", name="Usuario").fill("admin")
    page.get_by_role("textbox", name="Contraseña").click()
    page.get_by_role("textbox", name="Contraseña").click()
    page.get_by_role("textbox", name="Contraseña").fill("Admin123")
    page.get_by_role("textbox", name="Contraseña").press("Enter")
    page.get_by_role("link", name="Cerrar sesión").click()
    page.get_by_role("textbox", name="Usuario").click()
    page.get_by_role("textbox", name="Usuario").fill("admin")
    page.get_by_role("textbox", name="Usuario").press("Tab")
    page.get_by_role("textbox", name="Contraseña").fill("admin")
    page.get_by_role("textbox", name="Contraseña").press("Enter")
    page.get_by_role("textbox", name="Usuario").click()
    page.get_by_role("textbox", name="Usuario").fill("admin")
    page.get_by_role("textbox", name="Usuario").press("Tab")
    page.get_by_role("textbox", name="Contraseña").fill("Admin123")
    page.get_by_role("textbox", name="Contraseña").press("Enter")
    page.get_by_role("link", name="Nuevo producto").click()
    page.get_by_role("textbox", name="Nombre").click()
    page.get_by_role("textbox", name="Nombre").press("CapsLock")
    page.get_by_role("textbox", name="Nombre").fill("M")
    page.get_by_role("textbox", name="Nombre").press("CapsLock")
    page.get_by_role("textbox", name="Nombre").fill("Mousepad")
    page.get_by_role("textbox", name="Nombre").press("Tab")
    page.get_by_role("textbox", name="Precio").fill("20")
    page.get_by_role("textbox", name="Precio").press("Tab")
    page.get_by_role("textbox", name="Stock").fill("10")
    page.get_by_role("button", name="Guardar").click()
    page.get_by_role("row", name="1 Teclado 250.00 10 Editar").get_by_role("button").click()

#    Verifica el resultado esperado Y que no haya efectos colaterales
#    sobre los demás registros.
#
# Localizadores recomendados (por rol/etiqueta, como los ve el usuario):
#     page.get_by_label("Usuario").fill("admin")
#     page.get_by_role("button", name="Ingresar").click()
#     fila = page.get_by_role("row").filter(has_text="Teclado")
#     fila.get_by_role("button", name="Eliminar").click()
