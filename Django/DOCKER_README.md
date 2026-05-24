# 🐳 Guía de Dockerización - ERP Django

Este proyecto ha sido dockerizado para facilitar su despliegue y desarrollo. Aquí encontrarás las instrucciones para usar Docker.

## 📋 Requisitos Previos

- **Docker** (v20.10+) - [Instalar](https://docs.docker.com/get-docker/)
- **Docker Compose** (v1.29+) - Generalmente viene con Docker Desktop

Verifica la instalación:
```bash
docker --version
docker-compose --version
```

## 🚀 Inicio Rápido

### 1. **Actualizar requirements.txt**

Primero, actualiza tu `requirements.txt` con las nuevas dependencias (especialmente `gunicorn` y `python-decouple`):

```bash
pip install gunicorn python-decouple
pip freeze > requirements.txt
```

O reemplaza el archivo con:
```
asgiref==3.11.1
Django==6.0.5
djangorestframework==3.17.1
gunicorn==21.2.0
psycopg2-binary==2.9.12
python-decouple==3.8
sqlparse==0.5.5
tzdata==2026.2
```

### 2. **Crear archivo `.env`**

Copia el archivo de ejemplo y configura según tu entorno:

```bash
cp .env.example .env
```

Edita `.env` si necesitas cambiar valores (puertos, credenciales, etc.):

```env
DEBUG=False
SECRET_KEY=tu-clave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
DB_NAME=db_erp
DB_USER=postgres
DB_PASSWORD=admin
DB_HOST=db
DB_PORT=5432
APP_PORT=8000
```

### 3. **Construir e iniciar los contenedores**

```bash
# Construir las imágenes Docker
docker-compose build

# Iniciar los servicios (PostgreSQL y Django)
docker-compose up
```

Para ejecutar en segundo plano:
```bash
docker-compose up -d
```

### 4. **Verificar que todo funciona**

- Aplicación Django: [http://localhost:8000](http://localhost:8000)
- Admin de Django: [http://localhost:8000/admin](http://localhost:8000/admin)
- Base de datos: `localhost:5432`

## 📖 Comandos Útiles

### Iniciar/Detener Servicios

```bash
# Iniciar en primer plano
docker-compose up

# Iniciar en segundo plano
docker-compose up -d

# Detener servicios
docker-compose down

# Detener y eliminar datos (CUIDADO!)
docker-compose down -v
```

### Ejecutar Comandos Django

```bash
# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Migraciones
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Shell de Django
docker-compose exec web python manage.py shell

# Recopilar archivos estáticos
docker-compose exec web python manage.py collectstatic --noinput
```

### Ver Logs

```bash
# Todos los logs
docker-compose logs

# Logs en tiempo real
docker-compose logs -f

# Logs de un servicio específico
docker-compose logs -f web
docker-compose logs -f db
```

### Acceder a la Base de Datos

```bash
# Conectar a PostgreSQL
docker-compose exec db psql -U postgres -d db_erp

# O usando la línea de comandos
docker exec -it erp-postgres psql -U postgres -d db_erp
```

## 🔧 Estructura de Archivos Creados

```
├── Dockerfile              # Definición de la imagen Docker
├── docker-compose.yml      # Orquestación de servicios
├── .dockerignore          # Archivos a excluir en la imagen
├── entrypoint.sh          # Script de inicio del contenedor
├── .env.example           # Ejemplo de variables de entorno
└── requirements.txt       # (actualizado) Dependencias de Python
```

## 🐛 Solución de Problemas

### Error: "connection refused" a la base de datos

**Solución**: Espera a que PostgreSQL inicie. El `docker-compose.yml` incluye un `healthcheck` que espera a que esté lista.

```bash
# Ver estado de los servicios
docker-compose ps

# Ver logs de la BD
docker-compose logs db
```

### Error: "port already in use"

Si los puertos 8000 o 5432 ya están en uso:

```bash
# Cambiar en .env
APP_PORT=8001
DB_PORT=5433
```

O detener el servicio que usa el puerto:
```bash
# En Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# En Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Error: "ModuleNotFoundError: No module named 'decouple'"

Asegúrate de haber actualizado `requirements.txt` con `python-decouple==3.8`

### No se ve la aplicación en localhost:8000

```bash
# Verifica que los contenedores están corriendo
docker-compose ps

# Si no están, revisar errores
docker-compose logs web
```

## 🔐 Seguridad en Producción

**IMPORTANTE**: Antes de desplegar en producción:

1. **Generar nueva SECRET_KEY**:
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. **Cambiar DEBUG a False** en `.env`

3. **Usar contraseñas seguras** para la BD:
   ```env
   DEBUG=False
   SECRET_KEY=tu-clave-super-segura-aqui
   DB_PASSWORD=contraseña-fuerte-123!@#
   ```

4. **Configurar ALLOWED_HOSTS** con tu dominio:
   ```env
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

5. **Usar un servidor web** como Nginx en frente de Gunicorn

## 📦 Volúmenes Persistentes

El `docker-compose.yml` define dos volúmenes:

- **postgres_data**: Datos de la BD (persisten entre reinicios)
- **static_volume**: Archivos estáticos recopilados

## 🔄 Actualizar el Proyecto

```bash
# Si actualizas código
docker-compose up --build

# Si actualizas dependencias
docker-compose down
# Actualiza requirements.txt
docker-compose build
docker-compose up
```

## 🎓 Próximos Pasos

- Considera usar **Nginx** como proxy inverso
- Agregar **Redis** para caché
- Implementar **CI/CD** con GitHub Actions
- Usar **pgAdmin** para administrar PostgreSQL

---

¿Necesitas ayuda? Revisa los logs:
```bash
docker-compose logs -f
```
