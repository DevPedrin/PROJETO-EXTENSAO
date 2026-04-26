#  Portal Segurança Digital

Portal informativo para prevenção de golpes e acesso a conteúdos de
segurança digital.

------------------------------------------------------------------------

##  Membros

-   Elias Giovanni de Oliveira Brandão
-   Gabriel Victor Silva Vilarinho
-   Samuel Ulsan Cavalcante Luz
-   Wanderson das Neves Morais
-   Pedro Henrique Pereira Rocha

------------------------------------------------------------------------

##  Requisitos

-   Python
-   pip
-   PostgreSQL **ou** Docker + Docker Compose

------------------------------------------------------------------------

##  Setup

### 1. Clonar o projeto

``` bash
git clone https://github.com/DevPedrin/PROJETO-EXTENSAO
cd PROJETO-EXTENSAO
```

------------------------------------------------------------------------

### 2. Criar `.env`

``` bash
cp .env.example .env
```

O projeto já possui um `.env.example` configurado.

------------------------------------------------------------------------

### 3. Ambiente virtual

#### Linux/Mac

``` bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

``` bash
python -m venv venv
venv\Scripts\activate
```

------------------------------------------------------------------------

### 4. Instalar dependências

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

##  Banco de Dados

Escolha uma opção:

###  PostgreSQL local

-   Crie um banco (ex: `db-portal`)
-   Configure o `.env` conforme seu ambiente

------------------------------------------------------------------------

###  Docker

``` bash
docker-compose up -d
```

#### O banco será criado automaticamente.
------------------------------------------------------------------------

##  Migrations

``` bash
python manage.py migrate
```

------------------------------------------------------------------------

## ▶ Rodar o projeto

``` bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

------------------------------------------------------------------------

## ⚠️ Observações

-   O `.env` é obrigatório
-   O banco deve estar rodando antes das migrations
-   Não versionar o `.env`
