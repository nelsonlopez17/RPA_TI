# Usar imagen base Python 3.11
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . .

# Crear carpeta para archivos estáticos
RUN mkdir -p /app/staticfiles

# Permisos para el script de entrada
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Puerto por defecto
EXPOSE 8000

# Comando de entrada
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "configuracion_base.wsgi:application", "--bind", "0.0.0.0:8000"]
