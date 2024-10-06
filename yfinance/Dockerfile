# Imagem python
FROM python:3.9-slim

# Diretorio de trabalho
WORKDIR /app

# Copiar arquivos
COPY requirements.txt requirements.txt
COPY app.py app.py

# Instalar dependencias
RUN pip install -r requirements.txt

# Export a porta da API
EXPOSE 5000

# Iniciar app
CMD ["python" , "app.py"]