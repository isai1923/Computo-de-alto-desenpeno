# Resumen del Laboratorio 5.1: Trabajando con Amazon DynamoDB

## Objetivo General
El objetivo de este laboratorio es migrar la información del menú de la cafetería desde un archivo estático a una base de datos NoSQL gestionada, **Amazon DynamoDB**. El laboratorio se enfoca en crear una tabla, gestionar la inserción de datos (individual y por lotes), usar **expresiones condicionales** para evitar la sobrescritura de datos, y consultar la tabla usando tanto **AWS CLI** como el **SDK de AWS para Python (Boto3)**. Finalmente, se crea un **Índice Secundario Global (GSI)** para optimizar las consultas de atributos que no son clave.

---

## Tarea 1: Preparación del Laboratorio
Esta tarea se centra en configurar el entorno de desarrollo.
* **Conexión al IDE:** Acceder al IDE de VS Code proporcionado por el laboratorio.
* **Descarga de Archivos:** Descargar y descomprimir el archivo `code.zip`, que contiene los scripts de Python y los archivos JSON necesarios.
* **Verificación:** Ejecutar un script (`setup.sh`) para actualizar la AWS CLI y verificar que Boto3 esté instalado.

---

## Tarea 2: Crear una Tabla de DynamoDB (Boto3)
En esta tarea, se crea la estructura de la base de datos.
* **Definición de Esquema:** Editar el script `create_table.py` para definir la nueva tabla.
* **Creación de Tabla:** El script usa Boto3 para crear la tabla llamada `FoodProducts`.
* **Clave Primaria:** Se define `product_name` (un String) como la **clave primaria** (tipo HASH) de la tabla.
* **Verificación:** Se ejecuta el script y se verifica la creación de la tabla en la Consola de AWS y con el comando `aws dynamodb list-tables`.

---

## Tarea 3: Trabajar con Datos y Expresiones de Condición (CLI)
Aquí se explora el comportamiento fundamental de escritura de DynamoDB.
* **`put-item` (CLI):** Se usa el comando `aws dynamodb put-item` para insertar un elemento desde un archivo JSON.
* **Comportamiento de Sobrescritura:** Se descubre que si se ejecuta `put-item` con una clave primaria que ya existe, DynamoDB **sobrescribe** el elemento existente sin advertencia.
* **Solución (Expresión Condicional):** Para prevenir la sobrescritura accidental, se añade una **`ConditionExpression`** al comando: `"attribute_not_exists(product_name)"`.
* **Prueba:** Al intentar insertar un producto que ya existe con esta condición, el comando falla con un error `ConditionalCheckFailedException`, que es el comportamiento deseado para inserciones seguras.

---

## Tarea 4: Inserción Condicional con Boto3
Se aplica el concepto de la Tarea 3, pero esta vez usando el SDK de Python.
* **`put_item` (Boto3):** Se edita el script `conditional_put.py` para usar la operación `DDB.put_item`.
* **Protección de Datos:** El script incluye el parámetro `ConditionExpression='attribute_not_exists(product_name)'`.
* **Resultado:** El script puede añadir con éxito nuevos productos (como `apple pie`), pero falla si se intenta ejecutar dos veces con el mismo `product_name`, protegiendo los datos existentes.

---

## Tarea 5: Agregar Varios Elementos (Batch)
Esta tarea se centra en la carga masiva de datos, un escenario más realista.
* **Eliminación de Datos:** Se borran todos los elementos de la tabla para empezar la carga limpia.
* **`batch_writer` (Boto3):** Se utiliza el método `table.batch_writer()`.
* **Manejo de Duplicados (Prueba):** Se prueba primero con un archivo (`test.json`) que contiene duplicados.
    1.  Con `overwrite_by_pkeys`, el lote se completa, pero el último duplicado sobrescribe a los anteriores (comportamiento no deseado).
    2.  Se elimina `overwrite_by_pkeys`. El script ahora falla con una `ValidationException` (error de duplicados). Este es el comportamiento preferido para garantizar la integridad de los datos.
* **Carga de Producción:** Se usa el script final (`batch_put.py`) para cargar todos los datos de producción (desde `all_products.json`) en la tabla.

---

## Tarea 6: Consultar la Tabla (Boto3)
Ahora que los datos están cargados, se aprende a recuperarlos.
* **`scan()`:** Se edita `get_all_items.py`. Esta operación lee **toda la tabla**. El script también demuestra cómo manejar la **paginación** (usando `LastEvaluatedKey`) en caso de que los resultados superen 1 MB.
* **`get_item()`:** Se edita `get_one_item.py`. Esta operación es mucho más eficiente y se usa para obtener un **único elemento** especificando su clave primaria (`product_name: "chocolate cake"`).

---

## Tarea 7: Agregar un Índice Secundario Global (GSI)
Se aborda un requisito de negocio más complejo: optimizar las consultas.
* **Necesidad:** La cafetería quiere mostrar solo los productos "especiales" que están "en oferta". Consultar esto es ineficiente usando `scan` en toda la tabla, ya que "special" no es la clave primaria.
* **Solución:** Se crea un **Índice Secundario Global (GSI)**.
* **`update_table`:** Se usa el script `add_gsi.py` para añadir el GSI llamado `special_GSI` sobre el atributo `special` (un Número).
* **Consulta del GSI:** Se crea un script (`scan_with_filter.py`) que usa `table.scan()` pero especifica el `IndexName='special_GSI'`. Esto escanea eficientemente solo los elementos que tienen el atributo `special` (un índice disperso).
* **Filtro Adicional:** Se añade una `FilterExpression` a la consulta del GSI para excluir productos que tengan la etiqueta `out of stock`.