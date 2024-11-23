# Imagem python
FROM python:3.11-slim

# Diretorio de trabalho
WORKDIR /app

# Copiar arquivos
COPY requirements.txt requirements.txt
COPY . /app/

# Instalar dependencias
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Export a porta da API
EXPOSE 5000

# Iniciar app
CMD ["python" , "app.py"]