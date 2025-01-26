# Usa uma imagem Python como base
FROM python:3.12

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos para o container
COPY . /app

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta utilizada pela aplicação
EXPOSE 5000

# Define o comando para rodar a aplicação
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]