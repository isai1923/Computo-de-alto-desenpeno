# Resumen del Laboratorio 2.1: Explorando AWS CloudShell e IDE

## Objetivo General
El objetivo de este laboratorio es familiarizar al usuario  con dos entornos de desarrollo clave en AWS: **AWS CloudShell** y un **IDE de Visual Studio Code (VS Code)** basado en la nube. El laboratorio se centra en ejecutar comandos de AWS CLI, gestionar archivos en S3 y ejecutar scripts de Python (Boto3).


## Tarea 1: Explorar AWS CloudShell
En esta tarea se utiliza AWS CloudShell, un intérprete de comandos basado en navegador y preautenticado.

* **Acceso y Comandos CLI:** Inicia CloudShell directamente desde la Consola de Administración de AWS.
* **Verificación de AWS CLI:** Confirma que la AWS CLI v2 está instalada con el comando `aws --version`.
* **Interacción con S3 (CLI):** Lista los buckets de S3 existentes usando `aws s3 ls`.
* **Carga y Ejecución de Python (Boto3):**
    1.  Carga un archivo Python (`list-buckets.py`) a su entorno CloudShell.
    2.  Ejecuta el script con `python3 list-buckets.py` para listar programáticamente los buckets de S3, demostrando que Boto3 (el SDK de AWS para Python) está preinstalado.
* **Copia de Archivos a S3:** Utiliza el comando `aws s3 cp` para copiar el archivo `list-buckets.py` desde su entorno CloudShell a un bucket de S3.
---
## Tarea 2: Explorar el IDE de VS Code
A continuación, Sofía explora un entorno de desarrollo integrado (IDE) de VS Code más completo, alojado en una instancia de EC2.

* **Acceso al IDE:** Se conecta al IDE de VS Code proporcionado por el laboratorio usando una URL y una contraseña específicas.
* **Interacción con S3 (CLI):**
    1.  Utiliza el terminal Bash integrado en el IDE para listar buckets con `aws s3 ls`.
    2.  Copia el archivo `list-buckets.py` *desde* el bucket de S3 a su entorno local del IDE usando `aws s3 cp`.
* **Gestión de Dependencias (Boto3):**
    1.  Intenta ejecutar el script (`python3 list-buckets.py`), pero falla con un error `ModuleNotFoundError: No module named 'boto3'`.
    2.  A diferencia de CloudShell, debe instalar manualmente el SDK de Python.
    3.  Instala Boto3 usando `sudo pip3 install boto3`.
    4.  Vuelve a ejecutar el script, que ahora funciona correctamente.
* **Creación y Carga de Archivos:**
    1.  Crea un nuevo archivo llamado `index.html` directamente en el editor del IDE.
    2.  Añade el texto `<body> Hello World. </body>`.
    3.  Sube el nuevo archivo `index.html` al bucket de S3 usando `aws s3 cp`.
