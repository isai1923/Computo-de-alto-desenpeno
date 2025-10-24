# Resumen del Laboratorio 3.1: Trabajando con Amazon S3

## Objetivo General
El objetivo de este laboratorio es utilizar **Amazon S3** para alojar un sitio web estático para la cafetería. Las tareas clave incluyen crear un bucket, cargar los archivos del sitio web, y aplicar una **política de bucket** de seguridad para restringir el acceso al sitio solo a un rango de direcciones IP específico (en este caso, la IP del usuario).
---

## Tarea 1: Configuración del Entorno IDE
Esta tarea prepara el entorno de desarrollo de VS Code.

* **Conexión al IDE:** Acceder al IDE de VS Code basado en la nube usando la URL y contraseña proporcionadas por el laboratorio.
* **Instalación de Boto3:** Instalar el SDK de AWS para Python (Boto3) en el terminal del IDE usando el comando `sudo pip3 install boto3`.
* **Descarga de Archivos:** Descargar y descomprimir un archivo `code.zip` que contiene los recursos del sitio web (HTML, CSS, imágenes) y los scripts de Python necesarios para el laboratorio.

---

## Tarea 2: Creación y Configuración del Bucket S3
En esta tarea, se crea el bucket que alojará el sitio web.

* **Creación con CLI:** Utilizar la **CLI de AWS** en el terminal del IDE para crear un nuevo bucket de S3 único (p.ej., `sm-2022-08-26-s3site`) con el comando `aws s3api create-bucket`.
* **Modificación de Acceso Público:** Ir a la Consola de Administración de AWS, navegar al nuevo bucket y **editar la configuración de "Bloquear todo el acceso público"**. Se desmarca la casilla principal, pero se mantienen activas las sub-opciones para bloquear ACLs, preparando el bucket para una política de bucket específica.

---

## Tarea 3: Aplicación de Política de Bucket con Boto3
Esta es la tarea principal de seguridad. El objetivo es permitir el acceso de lectura (GetObject) solo desde la dirección IP del usuario.

* **Crear Política JSON:** Crear un archivo `website_security_policy.json` en el IDE.
* **Definir Política:** Pegar una política JSON que:
    * **Permite (`Allow`)** la acción `s3:GetObject` a cualquier principal (`*`).
    * **Restringe (`Condition`)** este permiso para que solo se aplique a las solicitudes originadas desde la dirección IP pública del usuario (`"aws:SourceIp": "<tu-ip-address>/32"`).
* **Aplicar con Python (Boto3):** Editar un script de Python (`permissions.py`) proporcionado para que apunte al nombre del bucket recién creado.
* **Ejecutar Script:** Correr el script `python3 permissions.py`. Este script utiliza Boto3 para leer el archivo JSON y aplicarlo como la política oficial del bucket S3.

---

## Tarea 4: Carga y Prueba del Sitio Web
Finalmente, se suben los archivos del sitio y se prueba la política de seguridad.

* **Carga Recursiva:** Usar la CLI de AWS para cargar de forma recursiva todos los archivos del sitio web desde el directorio local (`resources/website`) al bucket de S3 con el comando `aws s3 cp ... --recursive`.
* **Prueba de Éxito (Navegador):**
    1.  Obtener la URL del objeto `index.html` (p.ej., `https://<bucket-name>.s3.amazonaws.com/index.html`).
    2.  Pegar esta URL en el navegador. El sitio web se carga correctamente porque la solicitud proviene de la dirección IP permitida en la política.
* **Prueba de Fallo (Externa):**
    1.  Intentar acceder a la misma URL desde una red diferente (como un teléfono móvil en datos celulares) o usando el comando `curl` desde el terminal del IDE (que tiene una IP de servidor diferente).
    2.  Ambas pruebas fallan y devuelven un error **`AccessDenied`**, confirmando que la política de bucket está bloqueando correctamente el acceso no autorizado.