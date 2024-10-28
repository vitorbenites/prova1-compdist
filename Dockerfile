FROM python:3.12.7-alpine3.20

# Diretório da aplicação dentro do container
WORKDIR /app

# Variável do tipo do banco de dados
ENV DATABASE_TYPE=sqlite
ENV DATABASE_NAME=users

# Variável de chave do Flask
ENV SECRET_KEY=secret

# Variáveis de ambiente referentes as credenciais do banco de dados
ENV ADMIN_USER=admin
ENV ADMIN_PASSWORD=admin

# Variáveis de ambiente referentes ao mysql
ENV MYSQL_HOST=db_mysql
ENV MYSQL_PORT=3306

# Cópia do arquivo de dependências
COPY ./app/requirements.txt requirements.txt

# Download das dependências
RUN pip install --no-cache-dir -r requirements.txt

# Porta do serviço
EXPOSE 8080

# Cópia dos arquivos da aplicação
COPY ./app .

# Execução do serviço
CMD ["python","run.py"]
