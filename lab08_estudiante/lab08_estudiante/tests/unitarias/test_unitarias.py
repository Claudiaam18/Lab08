"""NIVEL UNITARIO (componente) — pytest puro.

Objeto de prueba: app/validaciones.py (funciones puras, sin servidor ni navegador).
Técnicas sugeridas: partición de equivalencia y análisis de valores límite.

Ejecuta solo este nivel:   pytest tests/unitarias -v
"""
import pytest

from app.validaciones import validar_credenciales, validar_producto


#validar_credenciales

def test_credenciales_con_formato_valido_no_tienen_errores():
    assert validar_credenciales("admin", "Admin123") == []


@pytest.mark.parametrize("usuario", ["", "   "])
def test_usuario_vacio_es_invalido(usuario):
    assert validar_credenciales(usuario, "Admin123") != []


@pytest.mark.parametrize("password, valido", [
    ("12345", False),   # último inválido: 5 caracteres
    ("123456", True),   # primer válido:   6 caracteres
])
def test_limite_longitud_password(password, valido):
    errores = validar_credenciales("admin", password)
    assert (errores == []) == valido


#validar_producto 

def test_producto_valido_no_tiene_errores():
    assert validar_producto("Teclado", 250.0, 10) == []


@pytest.mark.parametrize("nombre, valido", [
    ("ab", False),          # último inválido: 2 caracteres
    ("abc", True),          # primer válido:   3 caracteres
    ("a" * 50, True),       # último válido:   50 caracteres
    ("a" * 51, False),      # primer inválido: 51 caracteres
    ("  abc  ", True),      # espacios extremos no cuentan
])
def test_limites_nombre(nombre, valido):
    errores = validar_producto(nombre, 100.0, 0)
    assert (errores == []) == valido


@pytest.mark.parametrize("precio, valido", [
    (0,       False),   # último inválido: 0 (debe ser > 0)
    (0.01,    True),    # primer válido
    (100_000, True),    # último válido
    (100_001, False),   # primer inválido: supera el máximo
])
def test_limites_precio(precio, valido):
    errores = validar_producto("Teclado", precio, 0)
    assert (errores == []) == valido


@pytest.mark.parametrize("stock, valido", [
    (-1, False),    # último inválido
    (0,  True),     # primer válido
])
def test_limites_stock(stock, valido):
    errores = validar_producto("Teclado", 100.0, stock)
    assert (errores == []) == valido


# ------------------------------------------------------------------ TODO
# 1. validar_credenciales: usuario vacío, contraseña en el límite (5 y 6 caracteres).
# 2. validar_producto: un producto válido no tiene errores.
# 3. validar_producto: aplica VALORES LÍMITE a cada regla de la especificación
#    (nombre, precio y stock). Pregúntate: ¿cuál es el último valor inválido
#    y el primer valor válido de cada regla?
#
# Pista: @pytest.mark.parametrize evita repetir la misma prueba con datos distintos.
#
# @pytest.mark.parametrize("stock, valido", [(-1, False), (0, True)])
# def test_limites_de_stock(stock, valido):
#     errores = validar_producto("Teclado", 100.0, stock)
#     assert (errores == []) == valido
