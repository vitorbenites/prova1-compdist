# Prova 1 de Computação Distribuída

## Descrição 

Esta repositório fornece uma aplicação em Flask que funciona como uma página de administração, com suporte a autenticação básica e integração com banco de dados MySQL ou SQLite. A aplicação foi projetada para facilitar o gerenciamento de usuários e permitir a alternância entre bancos de dados por meio de variáveis de ambiente.

## Variáveis de ambiente

Abaixo estão as variáveis de ambiente utilizadas na aplicação, com breve explicação:

- `SECRET_KEY`: Chave secreta utilizada para proteção de sessão e autenticação do Flask;
- `DATABASE_TYPE`: Define o tipo de banco de dados a ser utilizado (`sqlite` ou `mysql`);
- `DATABASE_NAME`: Define o nome do banco de dados, tanto para `sqlite` ou `mysql`;
- `ADMIN_USER`: Nome do usuário administrador padrão, que será criado na inicialização da aplicação;
- `ADMIN_PASSWORD`: Senha do usuário administrador;
- `MYSQL_HOST`: Endereço do host onde o MySQL está executando;
- `MYSQL_PORT`: Porta do Mysql (padrão: `3306`);

## Build

Para construir a imagem docker da aplicação, o seguinte comando deve ser utilizado:

```bash
docker image build -t vitorbenites/compdistapp:1.0
```

O arquivo `docker-compose.yml` faz a construção da imagem e instância dos containers da aplicação e do banco de dados MySQL. \
Repositório da imagem: [vitorbenites/compdistapp:1.0](https://hub.docker.com/r/vitorbenites/compdistapp)

## Exemplos de uso

Abaixo estão dois exemplos de cenários para utilização da aplicação com diferentes configurações de banco de dados:

### Cenário 1: Utilizando SQLite

Docker run:

```bash
docker run -d -p 8080:8080 \
  -e SECRET_KEY=my_secret_key \
  -e DATABASE_TYPE=sqlite \
  -e DATABASE_NAME=usersdb \
  -e ADMIN_USER=admin \
  -e ADMIN_PASSWORD=admin \
  -v "$(pwd)/log:/app/log" \
  -v "$(pwd)/database:/app/database" \
  vitorbenites/compdistapp:1.0
```

Docker compose:

```yaml
services:
  app:
    image: vitorbenites/compdistapp:1.0
    container_name: compdistapp
    restart: unless-stopped
    environment:
      SECRET_KEY: secret_key
      DATABASE_TYPE: sqlite
      DATABASE_NAME: users
      ADMIN_USER: admin
      ADMIN_PASSWORD: admin
    volumes:
      - ./log:/app/log
      - ./database:/app/instance
    ports:
      - 8080:8080
```

### Cenário 2: Utilizando MySQL

Docker compose:

```yaml
services:
  app:
    image: vitorbenites/compdistapp:1.0
    container_name: compdistapp
    restart: unless-stopped
    environment:
      SECRET_KEY: secret_key
      DATABASE_TYPE: mysql
      DATABASE_NAME: users # Mesmo valor de MYSQL_DATABASE
      MYSQL_HOST: db_mysql
      MYSQL_PORT: "3306"
      ADMIN_USER: admin # Mesmo valor de MYSQL_USER
      ADMIN_PASSWORD: admin # Mesmo valor de MYSQL_PASSWORD
    volumes:
      - ./log:/app/log
    ports:
      - 8080:8080
    networks:
      - appnet
    depends_on:
      - db_mysql

  db_mysql:
    image: mysql:9.1
    container_name: compdistapp_db
    restart: always
    environment:
      MYSQL_DATABASE: users
      MYSQL_ROOT_PASSWORD: password
      MYSQL_USER: admin
      MYSQL_PASSWORD: admin
    volumes:
      - ./database:/var/lib/mysql
    ports:
      - 3306:3306
    networks:
      - appnet

networks:
  appnet:
    name: compdistapp_net
    driver: bridge
```
