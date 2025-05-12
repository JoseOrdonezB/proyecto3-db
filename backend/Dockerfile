# Usa imagen base oficial de Python
FROM python:3.10-slim

# Crea directorio de trabajo
WORKDIR /app

# Copia todo el contenido del backend
COPY . /app

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto donde correrá Flask
EXPOSE 8000

# Comando para ejecutar la app
CMD ["python", "app.py"]