# 1. La imagen base
FROM python:3.11-slim

# 2. Variables de entorno de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Instalación de paquetes del sistema operativo Linux
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# 4. Carpeta de trabajo dentro del contenedor
WORKDIR /app

# 5. Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar el código fuente
COPY . .

# 7. Documentación de puerto
EXPOSE 5678

# 8. Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5678"]
