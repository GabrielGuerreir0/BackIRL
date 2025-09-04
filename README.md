# FastAPI App com Docker e JWT

Esta é uma aplicação **FastAPI** construída com suporte a autenticação via **JWT**, utilizando **Docker** e um arquivo `.env` para configuração das variáveis de ambiente, incluindo `DATABASE_URL`.

---

## Tecnologias

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL (ou outro banco configurável via `DATABASE_URL`)
- JWT (JSON Web Tokens) para autenticação
- Docker & Docker Compose
- Pydantic para validação de dados

---

## Pré-requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## Estrutura do Projeto

```
├── app/
│   ├── api/
│   │   └── v1/        # Endpoints da API
│   ├── core/          # Configurações, JWT, settings
│   ├── crud/            # Configuração do banco
│   ├── db/          # Configurações, JWT, settings
│   ├── models/          # Configurações, JWT, settings
│   ├── uploads/          # Configurações, JWT, settings
│   └── main.py        # Ponto de entrada da aplicação
├── .env               # Variáveis de ambiente
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Configuração do `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
DATABASE_URL=postgresql+psycopg2://usuario:senha@db:5432/meubanco
```

> **Observação:** Ajuste `usuario`, `senha` e `meubanco` conforme sua configuração de banco de dados.

---

## Rodando a aplicação com Docker

1. Build e start dos containers:

```bash
docker-compose up --build
```

2. Acesse a API em:

```
http://localhost:8000
```

3. A documentação interativa estará disponível em:

```
http://localhost:8000/docs
```

---

## Comandos Úteis

- Parar os containers:

```bash
docker-compose down
```

- Rodar apenas o container da aplicação:

```bash
docker-compose up app
```

- Acessar o shell do container:

```bash
docker exec -it <nome_do_container> /bin/bash
```

---

## Estrutura de Autenticação JWT

- `POST /login`: Recebe usuário e senha e retorna token JWT.
- `Authorization: Bearer <token>`: Header necessário para acessar endpoints protegidos.

---

## Contribuição

Sinta-se à vontade para abrir issues e enviar pull requests!

---

## Licença

MIT License
