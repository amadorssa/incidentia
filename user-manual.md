# Incidentia Manual de Usuario

## Acceso al sistema
#### Navegar a la pagina principal:
   
   Abra su navegador web e ingrese la URL del sistema Incidentia en la barra de direcciones `http://148.225.83.8:8000/login/`

#### Acceso al formulario de inicio de sesión:
   
1. Será redirigido a una página con un formulario que contiene los siguientes campos:

   - Correo electrónico
   - Contraseña

#### Introducir las credenciales:

1. En el campo **correo electronico**, ingrese la dirección de correo asociada a su cuenta.
2. En el campo **contraseña**, ingrese la contraseña asignada al momento de registrarse.
3. Localiza y haz clic en el botón "Iniciar sesión" para continuar.

#### Validación de credenciales:

El sistema validará las credenciales ingresadas, donde se pueden presentar dos casos:

- **Credenciales correctas**: 
  
  Si las credenciales fueron validadas correctamente, el usuario será redirigido a la página *Mis organizaciones*.
- **Credenciales incorrectas**:
  
  Si las credenciales son incorrectas, el sistema mostrará el mensaje "*Credenciales incorrectas.*"
  En este caso, puede:
    1. Intentar ingresar nuevamente.
    2. Utilizar la opción `¿Olvidaste tu contraseña?` para recuperar su acceso.

#### Recuperación de contraseña:

Si olvidó su contraseña, puede recuperarla siguiendo estos pasos:

1. En la página de inicio de sesión, haga clic en la opción `¿Olvidaste tu contraseña?`.
2. Ingrese la dirección de correo electrónico asociada a su cuenta.
3. Presione `Enviar`. Recibirá un correo con instrucciones para restablecer su contraseña.

## Roles

En el sistema Incidentia, existen dos roles principales: Administrador y Usuario. Cada uno de ellos tiene permisos específicos que definen las acciones que pueden realizar dentro del sistema. A continuación, se describen las responsabilidades y capacidades de cada rol.

### Administrador

El rol de administrador es otorgado automáticamente al usuario que crea una nueva organización. Este rol tiene los permisos más altos dentro de la organización y puede gestionar tanto incidentes como usuarios.

#### Permisos:

Gestión de usuarios:

- Crear nuevas cuentas para otros usuarios.
- Asignar roles a los usuarios dentro de la organización.
- Dar de alta o eliminar usuarios de la organización.

Gestión de organizaciones:

- Modificar la información de la organización (nombre, descripción, etc.).
- Eliminar la organización si ya no es necesaria.

Gestión de incidentes:

- Crear, editar y eliminar incidentes registrados en la organización.
- Asignar incidentes a usuarios específicos para su resolución.
- Clasificar y priorizar incidentes según su gravedad o tipo.
- Visualización de información sensible:
- Acceder a todos los detalles de los incidentes, incluidos datos confidenciales.
- Consultar reportes completos de incidentes y estadísticas asociadas.

Historial de actividades:
- Revisar el registro de actividades realizadas por todos los usuarios de la organización.
- Supervisar intentos fallidos de inicio de sesión y otros eventos relevantes

### Usuario

El rol de usuario es asignado automáticamente al registrarse en una organización existente. Este rol tiene permisos limitados y se enfoca en el registro, seguimiento y resolución de incidentes dentro de la organización.

#### Permisos:

Gestión básica de incidentes:

- Registrar nuevos incidentes en el sistema.
- Editar los incidentes que haya creado personalmente.
- Agregar comentarios o actualizaciones sobre incidentes asignados a su nombre.

Acceso a información:

- Consultar información básica de los incidentes que les han sido asignados o que están disponibles para la organización.
- Visualizar su propio historial de actividades dentro del sistema.

Colaboración:
- Participar en la resolución de incidentes asignados por el administrador.
- Compartir observaciones o datos relevantes sobre los incidentes.

Restricciones:
- No puede modificar o eliminar incidentes creados por otros usuarios.
- No tiene acceso a datos confidenciales o estadísticos globales de la organización.
- No puede realizar cambios en la estructura de la organización ni gestionar usuarios.

## Estructura de bases de datos

#### Tabla *organizacion*

#### Tabla *usuario*