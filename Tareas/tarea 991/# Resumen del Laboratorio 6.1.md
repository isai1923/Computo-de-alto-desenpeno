# Resumen del Laboratorio 6.1: Desarrollando APIs REST con Amazon API Gateway

## Objetivo General
El objetivo de este laboratorio es crear la capa de Application Program Interface (API) para el sitio web de la cafetería usando **Amazon API Gateway**. En lugar de conectar la API directamente a la base de datos, se crearán **puntos de conexión simulados (mocks)**. Esto permite desarrollar y probar la API y la integración del front-end de forma independiente, antes de construir la lógica de backend (que se hará en el próximo laboratorio).
En este laboratorio, creará tres puntos de conexión simulados usando Boto3 (Python) para definir la API de forma programática:
1.  `[GET] /products`: Simulará la obtención de todos los productos.
2.  `[GET] /products/on_offer`: Simulará la obtención de solo los productos en oferta.
3.  `[POST] /create_report`: Simulará la solicitud de un informe.

---

## Tarea 1: Preparar el Entorno
Esta tarea configura el IDE y verifica el estado inicial del sitio web.

* **Conexión al IDE:** Acceder al IDE de VS Code proporcionado.
* **Descarga de Archivos:** Descargar y descomprimir el archivo `code.zip` con los scripts de Python.
* **Ejecutar `setup.sh`:** Este script instala Boto3 y despliega/actualiza el sitio web de la cafetería en S3. **Crucialmente, solicita la dirección IP del usuario** para actualizar la política del bucket S3 y permitir el acceso.
* **Verificación:** Cargar la URL del sitio web de S3 en un navegador. En este punto, el sitio funciona, pero está cargando los productos desde archivos JSON estáticos (p.ej., `all_products.json`) almacenados en el mismo bucket S3.

---

## Tarea 2: Crear el Primer Punto de Conexión (`[GET] /products`)
En esta tarea, se crea la API principal y el primer recurso.

* **Crear API (Boto3):** Editar y ejecutar el script `create_products_api.py`.
* **Acciones del Script:**
    1.  Crea la API REST principal llamada `ProductsApi`.
    2.  Añade el recurso `/products`.
    3.  Añade el método `GET` a `/products`.
    4.  Configura una **Integración Simulada (MOCK)**.
    5.  Define una **Plantilla de Respuesta** codificada que devuelve un JSON con 3 productos de muestra.
* **Prueba:** Ir a la consola de API Gateway, seleccionar la `ProductsApi` y usar el botón **Test** en el método `[GET] /products` para verificar que devuelve la respuesta JSON simulada de 3 productos.

---

## Tarea 3: Crear el Segundo Punto de Conexión (`[GET] /products/on_offer`)
Aquí se añade un recurso anidado para los productos en oferta.

* **Crear Recurso (Boto3):** Editar el script `create_on_offer_api.py`, proporcionando el `api_id` (de la `ProductsApi`) y el `parent_id` (del recurso `/products`).
* **Acciones del Script:**
    1.  Añade un recurso anidado: `/products/on_offer`.
    2.  Añade el método `GET` a este nuevo recurso.
    3.  Configura otra **Integración Simulada**, esta vez devolviendo un JSON con 1 producto de muestra.
* **Prueba:** Probar el nuevo método `[GET] /products/on_offer` en la consola de API Gateway y verificar que devuelve la respuesta simulada de 1 producto.

---

## Tarea 4: Crear el Tercer Punto de Conexión (`[POST] /create_report`)
Se añade un punto de conexión de tipo POST para una futura función de reportes.

* **Crear Recurso (Boto3):** Editar el script `create_report_api.py`, proporcionando el `api_id`.
* **Acciones del Script:**
    1.  Añade un recurso a nivel raíz: `/create_report`.
    2.  Añade el método `POST`.
    3.  Configura una **Integración Simulada** que devuelve un simple mensaje JSON: `{"msg_str": "report requested..."}`.
* **Prueba:** Probar el método `[POST] /create_report` en la consola de API Gateway.

---

## Tarea 5: Implementar la API
Para que la API sea accesible desde Internet, debe implementarse.

* **Implementar Etapa:** En la consola de API Gateway, seleccionar `ProductsApi` y usar la acción "Implementar API".
* **Crear Etapa:** Crear una **Nueva Etapa** llamada `prod`.
* **Copiar URL:** Una vez implementada, copiar la **URL de Invocación** (Invoke URL) de la etapa `prod`.

---

## Tarea 6: Actualizar el Sitio Web y Probar
El paso final es apuntar el sitio web de S3 a la nueva API implementada.

* **Actualizar `config.js`:** En el IDE de VS Code, editar el archivo `resources/website/config.js`. Pegar la **URL de Invocación** copiada en la variable `API_GW_BASE_URL_STR`.
* **Subir Configuración:** Ejecutar el script `update_config.py` (después de añadirle el nombre del bucket S3) para subir el archivo `config.js` actualizado al bucket.
* **Prueba Final:**
    1.  Actualizar la pestaña del navegador donde está el sitio web de la cafetería.
    2.  Observar (con las herramientas de desarrollador) que el sitio ya no carga los archivos JSON estáticos.
    3.  **Verificación:** La vista "on offer" (predeterminada) ahora muestra solo **1 producto** (del mock de `/on_offer`). Al hacer clic en "view all", se muestran solo **3 productos** (del mock de `/products`).

