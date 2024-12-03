# Imagem python
FROM python:3.11-slim

# Diretorio de trabalho
WORKDIR /app

# Copiar arquivos
COPY requirements.txt requirements.txt
COPY app.py /app/
COPY modelo/lstm.h5 modelo/
COPY static /app/static

# Instalar dependencias
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Export a porta da API
EXPOSE 8080

# Iniciar app
CMD ["python" , "app.py"]