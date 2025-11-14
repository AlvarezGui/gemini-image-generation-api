# Imagem base
FROM python:3.12-slim

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Evitar arquivos de cache do Python
ENV PYTHONUNBUFFERED=1

# Copiar apenas requirements primeiro (para cache)
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do projeto
COPY . .

# Expor porta caso seu main.py use Flask
EXPOSE 5000

# Rodar o aplicativo Python
CMD ["python", "main.py"]
