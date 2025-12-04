PLAN DE PRUEBAS - SISTEMA DE GESTIÓN DE INVENTARIO
Información del Proyecto
Proyecto: Sistema de Gestión de Inventario
Asignatura: Pruebas de Software
Fecha: Diciembre 2025
Versión: 1.0
Objetivo
Validar el correcto funcionamiento del sistema de gestión de inventario, garantizando que todas las funcionalidades cumplan con los requisitos establecidos y que el sistema sea robusto, seguro y confiable.

PRUEBAS UNITARIAS
PU-001: Crear Categoría Exitosamente
Tipo: Unitaria
Descripción: Valida la creación correcta de una categoría con datos válidos
Prerrequisitos: Base de datos limpia
Pasos:
Llamar a CategoryService.create_category("Electrónica")
Verificar que se retorna un objeto Category
Resultado Esperado: Categoría creada con ID asignado y nombre "Electrónica"
Resultado Obtenido: ✓ Exitoso
PU-002: Crear Categoría con Nombre Vacío
Tipo: Unitaria
Descripción: Valida que no se permita crear categoría sin nombre
Prerrequisitos: Base de datos limpia
Pasos:
Llamar a CategoryService.create_category("")
Capturar excepción
Resultado Esperado: ValueError con mensaje "El nombre de la categoría es requerido"
Resultado Obtenido: ✓ Exitoso
PU-003: Crear Categoría Duplicada
Tipo: Unitaria
Descripción: Valida que no se permitan categorías con nombres duplicados
Prerrequisitos: Categoría "Electrónica" ya existe
Pasos:
Crear categoría "Electrónica"
Intentar crear otra categoría "Electrónica"
Resultado Esperado: ValueError con mensaje "Ya existe una categoría con ese nombre"
Resultado Obtenido: ✓ Exitoso
PU-004: Obtener Todas las Categorías
Tipo: Unitaria
Descripción: Valida la obtención del listado completo de categorías
Prerrequisitos: Dos categorías creadas
Pasos:
Crear "Electrónica" y "Ropa"
Llamar a CategoryService.get_all_categories()
Resultado Esperado: Lista con 2 categorías
Resultado Obtenido: ✓ Exitoso
PU-005: Actualizar Categoría
Tipo: Unitaria
Descripción: Valida la actualización del nombre de una categoría
Prerrequisitos: Categoría existente
Pasos:
Crear categoría "Electrónica"
Actualizar a "Tecnología"
Resultado Esperado: Categoría actualizada correctamente
Resultado Obtenido: ✓ Exitoso
PU-006: Eliminar Categoría
Tipo: Unitaria
Descripción: Valida la eliminación de una categoría sin productos
Prerrequisitos: Categoría sin productos asociados
Pasos:
Crear categoría
Eliminar categoría
Resultado Esperado: Categoría eliminada, retorna True
Resultado Obtenido: ✓ Exitoso
PU-007: Crear Producto Exitosamente
Tipo: Unitaria
Descripción: Valida la creación correcta de un producto
Prerrequisitos: Categoría existente
Pasos:
Crear categoría
Crear producto con datos válidos
Resultado Esperado: Producto creado con todos los campos correctos
Resultado Obtenido: ✓ Exitoso
PU-008: Crear Producto con Precio Negativo
Tipo: Unitaria
Descripción: Valida que no se permitan precios negativos
Prerrequisitos: Categoría existente
Pasos:
Intentar crear producto con precio -100
Resultado Esperado: ValueError "El precio debe ser un valor positivo"
Resultado Obtenido: ✓ Exitoso
PU-009: Crear Producto con Stock Negativo
Tipo: Unitaria
Descripción: Valida que no se permita stock negativo
Prerrequisitos: Categoría existente
Pasos:
Intentar crear producto con stock -5
Resultado Esperado: ValueError "El stock debe ser un valor positivo"
Resultado Obtenido: ✓ Exitoso
PU-010: Actualizar Producto
Tipo: Unitaria
Descripción: Valida la actualización de datos de un producto
Prerrequisitos: Producto existente
Pasos:
Crear producto
Actualizar nombre, precio y stock
Resultado Esperado: Producto actualizado correctamente
Resultado Obtenido: ✓ Exitoso
PRUEBAS DE INTEGRACIÓN
PI-001: API - Crear Categoría
Tipo: Integración
Descripción: Valida el endpoint POST /api/categories
Prerrequisitos: Servidor API en ejecución
Pasos:
Enviar POST a /api/categories con {"name": "Electrónica"}
Verificar respuesta
Resultado Esperado: Status 201, JSON con id y nombre
Resultado Obtenido: ✓ Exitoso
PI-002: API - Listar Categorías
Tipo: Integración
Descripción: Valida el endpoint GET /api/categories
Prerrequisitos: Dos categorías en la BD
Pasos:
Crear dos categorías
Enviar GET a /api/categories
Resultado Esperado: Status 200, array con 2 elementos
Resultado Obtenido: ✓ Exitoso
PI-003: API - Obtener Categoría por ID
Tipo: Integración
Descripción: Valida el endpoint GET /api/categories/:id
Prerrequisitos: Categoría existente
Pasos:
Crear categoría
Enviar GET a /api/categories/{id}
Resultado Esperado: Status 200, datos de la categoría
Resultado Obtenido: ✓ Exitoso
PI-004: API - Actualizar Categoría
Tipo: Integración
Descripción: Valida el endpoint PUT /api/categories/:id
Prerrequisitos: Categoría existente
Pasos:
Crear categoría
Enviar PUT con nuevo nombre
Resultado Esperado: Status 200, categoría actualizada
Resultado Obtenido: ✓ Exitoso
PI-005: API - Eliminar Categoría
Tipo: Integración
Descripción: Valida el endpoint DELETE /api/categories/:id
Prerrequisitos: Categoría sin productos
Pasos:
Crear categoría
Enviar DELETE a /api/categories/{id}
Resultado Esperado: Status 200, mensaje de éxito
Resultado Obtenido: ✓ Exitoso
PI-006: API - Crear Producto
Tipo: Integración
Descripción: Valida el endpoint POST /api/products
Prerrequisitos: Categoría existente
Pasos:
Crear categoría
Enviar POST a /api/products con datos completos
Resultado Esperado: Status 201, producto creado
Resultado Obtenido: ✓ Exitoso
PI-007: API - Listar Productos
Tipo: Integración
Descripción: Valida el endpoint GET /api/products
Prerrequisitos: Productos en la BD
Pasos:
Crear varios productos
Enviar GET a /api/products
Resultado Esperado: Status 200, array de productos
Resultado Obtenido: ✓ Exitoso
PI-008: API - Filtrar Productos por Categoría
Tipo: Integración
Descripción: Valida filtrado de productos por categoría
Prerrequisitos: Productos de diferentes categorías
Pasos:
Crear productos en diferentes categorías
Enviar GET a /api/products?category_id={id}
Resultado Esperado: Solo productos de esa categoría
Resultado Obtenido: ✓ Exitoso
PI-009: API - Health Check
Tipo: Integración
Descripción: Valida el endpoint de salud del sistema
Prerrequisitos: Servidor ejecutándose
Pasos:
Enviar GET a /health
Resultado Esperado: Status 200, {"status": "healthy"}
Resultado Obtenido: ✓ Exitoso
PRUEBAS END-TO-END (E2E)
PE-001: Flujo Completo - Crear Categoría, Producto y Visualizar
Tipo: E2E / Sistema
Descripción: Valida el flujo completo de usuario desde la interfaz web
Prerrequisitos:
Backend ejecutándose en localhost:5000
Frontend ejecutándose en localhost:3000
ChromeDriver instalado
Pasos:
Abrir navegador en localhost:3000/categories
Ingresar "Electrónica E2E" en el campo nombre
Click en botón "Crear Categoría"
Verificar que aparece en la tabla
Navegar a /products
Llenar formulario: nombre="Laptop E2E", categoría="Electrónica E2E", precio=1500, stock=10
Click en "Crear Producto"
Verificar que aparece en la tabla con todos los datos
Resultado Esperado:
Categoría visible en tabla de categorías
Producto visible en tabla de productos
Datos mostrados correctamente
Resultado Obtenido: ✓ Exitoso
PE-002: Navegación Entre Páginas
Tipo: E2E / Sistema
Descripción: Valida la navegación correcta entre las páginas del sistema
Prerrequisitos: Frontend ejecutándose
Pasos:
Abrir página principal
Click en "Categorías"
Verificar URL contiene /categories
Click en "Productos"
Verificar URL contiene /products
Click en "Inicio"
Verificar URL es raíz
Resultado Esperado: Navegación fluida entre páginas
Resultado Obtenido: ✓ Exitoso
PE-003: Carga de Página de Inicio
Tipo: E2E / Sistema
Descripción: Valida que la página principal carga correctamente
Prerrequisitos: Frontend ejecutándose
Pasos:
Abrir localhost:3000
Verificar título de página
Verificar presencia de elementos hero
Resultado Esperado: Página carga con todos los elementos
Resultado Obtenido: ✓ Exitoso
ANÁLISIS ESTÁTICO
AE-001: Análisis con Flake8
Tipo: Análisis Estático
Descripción: Verificar calidad de código Python
Prerrequisitos: Código fuente disponible
Pasos:
Ejecutar flake8 backend/ frontend/
Resultado Esperado: Sin errores de estilo PEP8
Resultado Obtenido: ✓ Exitoso
AE-002: Análisis de Seguridad con Bandit
Tipo: Análisis Estático de Seguridad
Descripción: Identificar vulnerabilidades de seguridad
Prerrequisitos: Código fuente disponible
Pasos:
Ejecutar bandit -r backend/
Resultado Esperado: Sin vulnerabilidades críticas
Resultado Obtenido: ✓ Exitoso
RESUMEN DE RESULTADOS
Tipo de Prueba	Total	Exitosas	Fallidas	Porcentaje
Unitarias	10	10	0	100%
Integración	9	9	0	100%
E2E	3	3	0	100%
Análisis Estático	2	2	0	100%
TOTAL	24	24	0	100%
COBERTURA DE CÓDIGO
Backend: >85% de cobertura
Servicios: 100% de cobertura
Controladores: 95% de cobertura
Modelos: 90% de cobertura
CONCLUSIONES
El sistema de gestión de inventario ha pasado satisfactoriamente todas las pruebas automatizadas, demostrando:

✓ Funcionalidad completa de CRUD para categorías y productos
✓ Validaciones correctas de datos de entrada
✓ Integración exitosa entre backend y frontend
✓ Interfaz de usuario funcional
✓ Código cumple con estándares de calidad (PEP8)
✓ Sin vulnerabilidades de seguridad detectadas
✓ Pipeline de CI/CD funcionando correctamente
El sistema está listo para su uso en producción.

Fecha de Última Actualización: Diciembre 2025
Responsable: Estudiante de Ingeniería de Software
Estado: Aprobado ✓

