FROM python:3.12-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo
WORKDIR /app

# Actualiza y instala las dependencias necesarias
# Actualiza y instala las dependencias necesarias
RUN apt-get update && apt-get install -y \
    poppler-utils \
    ghostscript \
    libpq-dev \
    gcc \
    apt-transport-https \
    libgl1-mesa-dev \
    libglib2.0-0 \
    ffmpeg \
    libsm6 \
    curl \
    libxext6 \
    libxrender-dev \
    v4l-utils \
    && rm -rf /var/lib/apt/lists/*

# Copia y instala los requisitos de Python
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copia el código de la aplicación
COPY ./app /app/app

# COPY ./app/static /app/app/static
# Establece la variable de entorno PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app/app"

# Comando para iniciar la aplicación
CMD ["uvicorn", "app.main:api", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
