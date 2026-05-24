# ⚡ Inicio Rápido - Docker

## Pasos para ejecutar la aplicación con Docker en 2 minutos:

### 1️⃣ Crear archivo `.env`
```bash
cp .env.example .env
```

### 2️⃣ Construir y ejecutar
```bash
docker-compose up --build
```

### 3️⃣ ¡Listo!
Accede a: [http://localhost:8000](http://localhost:8000)

---

## Comandos Principales

| Comando | Descripción |
|---------|-------------|
| `docker-compose up` | Iniciar servicios |
| `docker-compose down` | Detener servicios |
| `docker-compose logs -f` | Ver logs en tiempo real |
| `docker-compose exec web python manage.py createsuperuser` | Crear admin |
| `docker-compose ps` | Ver estado de servicios |

---

## Si tienes Makefile instalado:

```bash
make up              # Iniciar
make down            # Detener
make logs            # Ver logs
make createsuperuser # Crear usuario admin
make shell           # Shell de Django
```

---

⚠️ **Nota**: Necesitas actualizar `requirements.txt` con:
- gunicorn
- python-decouple

Ver [DOCKER_README.md](DOCKER_README.md) para guía completa.
