# Configuración del software

Incidentia es un sistema de gestión de incidentes desarrollado en Django. Este proyecto permite a las organizaciones registrar, monitorear y gestionar incidentes de manera eficiente, facilitando la toma de decisiones y mejorando la respuesta ante incidentes.

## Características

- **Gestión de incidentes**: Registro y administración de incidentes con detalles específicos y asignación de responsables.
- **Gestión de cuentas**: Sistema de autenticación de usuarios con roles y permisos diferenciados.
- **Gestión de organizaciones**: Módulo para administrar datos de diferentes organizaciones.
- **Subida de archivos**: Permite adjuntar documentos y archivos multimedia relevantes a cada incidente.
- **Dashboard**: Visualización de estadísticas y métricas clave para un mejor monitoreo.

## Estructura del Proyecto

El proyecto está organizado en los siguientes directorios y archivos principales:

- **`manage.py`**: Herramienta de línea de comandos para interactuar con la aplicación Django.
- **`db.sqlite3`**: Base de datos SQLite utilizada para almacenar los datos de incidentes y usuarios.
- **`incidents/`**: Aplicación principal que contiene la lógica de gestión de incidentes.
- **`cuentas/`**: Aplicación de gestión de cuentas de usuario, incluyendo login, registro y perfiles.
- **`organizaciones/`**: Aplicación para la administración de datos de organizaciones.
- **`media/`**: Directorio para el almacenamiento de archivos multimedia subidos por los usuarios.
- **`mysite/`**: Configuración principal del proyecto Django.
- **`requirements.txt`**: Archivo que lista todas las dependencias necesarias para ejecutar el proyecto.

## Instalación

1. Clona este repositorio:
   ```bash
   git clone <URL_del_repositorio>
   cd incidentia
    ```

2. Crea un entorno virtual y actívalo:
    ```bash
    python3 -m venv env
    source env/bin/activate  # En Windows: env\Scripts\activate
    ```
3. Instala las dependencias del proyecto:
    ```bash
    pip install -r requirements.txt
    ```
4. Realiza las migraciones de la base de datos:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5. Initializa el servidor de desarrollo:
    ```bash
    python manage.py runserver
    ```

## Uso

Una vez que el servidor esté en funcionamiento, dirigete a `http://127.0.0.1:8000/login` en tu navegador para acceder a la aplicación y comenzar a gestionar incidentes.

## Contribución


1. Realiza un fork del proyecto.
2. Crea una nueva rama con tu funcionalidad: git checkout -b nueva-funcionalidad
3. Realiza un commit de tus cambios: git commit -m 'Añadir nueva funcionalidad'
4. Sube tus cambios a la rama: git push origin nueva-funcionalidad
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT.

## Autores
- Camargo Loaiza, Julio Andres [Administrador del proyecto]
- Beltran Uvamea, Jesus Raul [Desarrollador]
- Rosas Archiveque, Amado [Desarrollador]
- Ortega Caudillo, Ricardo Emanuel [Desarrollador]
- Peña del Castillo, Francisco Aureliano [Desarrollador]

___
Repositorio disponible en [GitHub](https://github.com/amadorssa/incidentia)