FROM python:3.13

# Diretório da aplicação dentro do container
WORKDIR /app

# Variável do tipo do banco de dados
ENV DATABASE_TYPE=sqlite
ENV DATABASE_NAME=users
ENV DATABASE_URL=sqlite:///${DATABASE_NAME}.sqlite3

# Variável de chave do Flask
ENV SECRET_KEY=secret

# Variáveis de ambiente referentes as credenciais do banco de dados
ENV ADMIN_USER=admin
ENV ADMIN_PASSWORD=admin

# Variáveis de ambiente referentes ao mysql
ENV MYSQL_HOST=db_mysql # Nome do container do MySQL
ENV MYSQL_PORT=3306 # Porta do container do MySQL
ENV DATABASE_URL_MYSQL=mysql://${ADMIN_USER}:${ADMIN_PASSWORD}@${MYSQL_HOST}:${MYSQL_PORT}/${DATABASE_NAME}

# Cópia do arquivo de dependências
COPY ./app/requirements.txt requirements.txt

# Download das dependências
RUN pip install --no-cache-dir -r requirements.txt

# Porta do serviço
EXPOSE 8080

# Cópia dos arquivos da aplicação
COPY ./app .

# Execução do serviço
CMD ["python","app.py"]
