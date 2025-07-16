FROM python:3.9-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código, incluyendo el script wait-for-it.sh
COPY . .

# Dar permisos de ejecución al script
RUN chmod +x wait-for-it.sh

# Exponer el puerto del servicio
EXPOSE 4007

# Comando para ejecutar la app, esperando que la DB esté lista
CMD ["./wait-for-it.sh", "appointment-db:5432", "--", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "4007"]
