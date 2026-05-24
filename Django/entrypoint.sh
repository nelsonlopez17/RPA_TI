#!/bin/bash

set -e

# Intentar esperaR a PostgreSQL (solo si pg_isready está disponible)
if command -v pg_isready &> /dev/null; then
    echo "Esperando a que PostgreSQL esté listo..."
    for i in {1..30}; do
        if pg_isready -h ${DB_HOST:-localhost} -p ${DB_PORT:-5432} -U ${DB_USER:-postgres} > /dev/null 2>&1; then
            echo "PostgreSQL está listo"
            break
        fi
        echo "Intento $i/30 - esperando..."
        sleep 2
    done
fi

# Aplicar migraciones
echo "Aplicando migraciones..."
python manage.py migrate --noinput || echo "⚠️ Error en migraciones (continuando...)"

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear || echo "⚠️ Error en collectstatic (continuando...)"

# Ejecutar comando pasado como argumento
echo "Iniciando aplicación..."
exec "$@"
