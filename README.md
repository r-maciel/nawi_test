# NAWI Test
Solución al reto técnico de Nawi

## Reqisitos
- Docker

## Como instalar
1. Clona el repositorio
2. Ejecuta el comando `docker-compose up --build`, esto construirá el contenedor y ejecutará la aplicación
3. Ingresa a http://127.0.0.1:8001/docs desde tu navegador

## Enpoints
El proyecto cuenta con 5 endpoints

### \[POST\] /users
Este enpoint se encarga de crear un usuario, el `username` debe de ser único, en caso de que ya exista, mostrará un error

### \[POST\] /login
Una vez creado tu usuario, podrás acceder a esta ruta con tu username y password, te devolverá:
 - access_token: Con este podrás hacer peticiones (tiene una vida útil de 1 minuto)
 - refresh_token: Este lo necesitarás en caso de querer regenerar tu access_token (tiene una vida útil de 3 minutos)

### \[POST\] /verify
En este endpoint podrás verificar tu access_token para corroborar que sigue siendo válido


### \[POST\] /refresh
Aquí podrás regenerar tu acces_token, necesitaras tu refresh_token

### \[POST\] /logout
El access token entrará en un blacklist, de modo que ya no lo podrás usar aunque aún no haya caducado, tendrás que generar otro.

## Sobre el proyecto
- Tomé la decisión de usar post y mandar en el body los tokens para facilitar el testeo manual de la API.
- En la carpeta `models` se encuentran los modelos correspondientes a las tablas de la BD
- En `utils` está el código que suele ser repetitivo y no tiene que ver directamente con como se muestran los datos en los endpoints.
- Dentro de `routers` están las rutas a los endpoints, separadas por su funcionalidad
- La conexión a la DB se encuentra en el archivo `db.py`
- En `settings.py` se encuentra el punto de entrada para obtener datos a partir de variables de entorno
- El archivo `.env` no debería de colocarse en entornos productivos dentro del repositorio, pero para efectos prácticos lo he dejado.
