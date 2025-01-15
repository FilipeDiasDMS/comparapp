# Use uma imagem base do Python
FROM python:3

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o arquivo requirements.txt e instale as dependências
COPY requirements.txt .

RUN python3 -m venv /venv
RUN /venv/bin/pip install -r requirements.txt
# Dependências necessárias para o Matplotlib em ambientes headless
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libxft-dev \
    libpng-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


# Copie o resto da aplicação
COPY . .

# Comando para iniciar a aplicação
CMD ["/venv/bin/python", "main.py"]

