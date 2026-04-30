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

```bash
cp .env.example .env
```

O projeto já possui um `.env.example` configurado.

---

## Ambiente de execução

Escolha uma das opções abaixo.

## Opção 1: Docker (recomendado)

Subir containers:

```bash
docker compose up --build -d
```

Acesse:

http://127.0.0.1:8000/

### Aplicar migrations

Sempre que houver alteração nos models ou após atualizar o projeto:

```bash
docker compose exec application python manage.py migrate
```

---

## Opção 2: Execução local

### 3. Criar ambiente virtual

#### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Banco de Dados

### PostgreSQL local

- Crie um banco (exemplo: `db-portal`)
- Configure o arquivo `.env`

---

## Aplicar migrations

```bash
python manage.py migrate
```

---

## Rodar o projeto

```bash
python manage.py runserver
```

Acesse:

http://127.0.0.1:8000/

---

## Observações

- O arquivo `.env` é obrigatório
- O banco deve estar rodando antes das migrations
- Não versionar o `.env`
- O projeto pode ser executado com ou sem Docker