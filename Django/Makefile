.PHONY: help build up down logs shell migrate createsuperuser collectstatic clean

help:
	@echo "Comandos disponibles:"
	@echo "  make build              - Construir imágenes Docker"
	@echo "  make up                 - Iniciar servicios"
	@echo "  make down               - Detener servicios"
	@echo "  make logs               - Ver logs en tiempo real"
	@echo "  make shell              - Acceder al shell de Django"
	@echo "  make migrate            - Ejecutar migraciones"
	@echo "  make createsuperuser    - Crear superusuario"
	@echo "  make collectstatic      - Recopilar archivos estáticos"
	@echo "  make dbshell            - Acceder a PostgreSQL"
	@echo "  make clean              - Limpiar contenedores y volúmenes"
	@echo "  make restart            - Reiniciar servicios"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✓ Servicios iniciados"
	@echo "  Django: http://localhost:8000"
	@echo "  Admin: http://localhost:8000/admin"

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec web python manage.py shell

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

dbshell:
	docker-compose exec db psql -U postgres -d db_erp

clean:
	docker-compose down -v
	@echo "✓ Contenedores y volúmenes eliminados"

restart:
	docker-compose restart

status:
	docker-compose ps

install-deps:
	docker-compose exec web pip install -r requirements.txt

bash:
	docker-compose exec web bash

test:
	docker-compose exec web python manage.py test

format:
	docker-compose exec web black .
	docker-compose exec web isort .
