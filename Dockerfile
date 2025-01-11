# Use uma imagem base do Python
FROM python:3.9-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo requirements.txt e instale as dependências
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copie o resto da aplicação
COPY . .

# Comando para iniciar a aplicação
CMD ["python", "Comparapp_nofastapi.py"]  # Altere "Comparapp.py" pelo nome do seu arquivo principal

