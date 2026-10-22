# Informe · Laboratorio 8 · Pruebas automatizadas

**Equipo:** 
**Integrantes:** Tony Balán - 1202124
                 Claudia Mejía - 1127224

## 1. Defectos encontrados

Un reporte por defecto. Deja la prueba que lo detecta FALLANDO en tu entrega.

| ID | Nivel que lo detectó | Prueba (archivo::función) | Pasos para reproducir | Resultado esperado (según la especificación) | Resultado obtenido |
|---|---|---|---|---|---|
| DEF-01 | Unitario | `tests/unitarias/test_unitarias.py::test_limites_precio[0-False]` | Llamar `validar_producto("Teclado", 0, 5)` directamente en Python | Lista con al menos un mensaje de error (precio 0 no es mayor que 0) | Lista vacía — la función acepta precio 0 como válido |
| DEF-02 | API | `tests/api/test_api.py::test_obtener_producto_inexistente_devuelve_404` | Autenticarse y hacer `GET /api/productos/999` con token válido | HTTP 404 | HTTP 200 con cuerpo `{}` |
| DEF-03 | E2E | `tests/e2e/test_e2e.py::test_eliminar_producto_no_afecta_los_demas[chromium]` | 1. Login como admin. 2. Hacer clic en "Eliminar" en la fila de "Mouse". 3. Verificar que "Teclado" sigue visible en la tabla. | Solo "Mouse" desaparece; "Teclado" y "Monitor" permanecen en la tabla | "Mouse" no desaparece de la tabla tras eliminar — el botón eliminar no funciona correctamente |

## 2. Tabla comparativa de niveles

Tiempo: ejecuta `pytest tests/<nivel> -q` y anota el tiempo que reporta pytest.

| Criterio | Unitarias | API | E2E |
|---|---|---|---|
| Número de pruebas | 17 | 13 | 7 |
| Tiempo total de ejecución (s) | 0.33 | 0.83 | 8.72 |
| Tiempo promedio por prueba (s) | 0.02 | 0.06 | 1.25 |
| Defectos detectados (IDs) | DEF-01 | DEF-02 | DEF-03 |
| ¿Qué cambio en la app rompería estas pruebas sin que haya un defecto? | Renombrar las funciones `validar_credenciales` o `validar_producto` | Cambiar la URL base o el formato del JSON de respuesta | Cambiar el texto de botones, etiquetas o mensajes flash en el HTML |
| Costo de mantenimiento (Alto / Medio / Bajo) y por qué | Bajo — prueban funciones puras sin dependencias externas | Medio — dependen del contrato HTTP; cambian si cambia la API | Alto — dependen de la UI; cualquier cambio visual puede romperlas |

## 3. Recomendación (máximo media página)

El equipo de Inventario IS1 tiene un pipeline de CI. Recomienda qué pruebas correr:

- en cada commit,
- en cada pull request,
- antes de liberar a producción.

Justifica con tus datos de la tabla y con la pirámide de pruebas.
Responde además: ¿qué defecto NO habría detectado una suite solo de pruebas E2E, o solo de pruebas unitarias?

### Recomendación

**En cada commit:** correr solo las pruebas unitarias (`pytest tests/unitarias`). Con 0.33 s de ejecución y costo de mantenimiento bajo, dan retroalimentación inmediata sobre las reglas de negocio sin necesitar servidor ni navegador.

**En cada pull request:** agregar las pruebas de API (`pytest tests/unitarias tests/api`). El tiempo combinado es menor a 1.2 s y verifican el contrato HTTP completo. Detectaron DEF-02, que las unitarias no pueden ver porque requiere levantar el servidor.

**Antes de liberar a producción:** correr la suite completa (`pytest`), incluyendo E2E. Las pruebas E2E son las más lentas (8.72 s, ~1.25 s por prueba) y frágiles, pero son las únicas que detectaron DEF-03: un efecto colateral en la interfaz que no era visible ni en las funciones puras ni en el contrato HTTP.

Esto sigue la **pirámide de pruebas**: muchas pruebas unitarias (rápidas y baratas) en la base, menos de API en el medio, y pocas E2E en la cima. Invertir la pirámide (solo E2E) habría dejado DEF-01 sin detectar, ya que la interfaz web no expone directamente el valor límite `precio = 0` como caso de prueba aislado. Del mismo modo, una suite solo unitaria nunca habría encontrado DEF-02 ni DEF-03, que requieren servidor y navegador respectivamente.
