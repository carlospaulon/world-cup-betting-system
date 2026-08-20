# World Cup Betting System - PalpiteCopa

Sistema completo de apostas e palpites esportivos voltado para a Copa do Mundo 2026 e o Brasileirão. O projeto conta com um backend em FastAPI, inteligência artificial para predição de partidas com Machine Learning, pipeline de exportação de dados analíticos e um frontend responsivo em React.

---

## Aplicação em Produção (Deploy - Render)

Acesse o sistema online através dos links abaixo:

- **Frontend Web (Aplicação):** [https://world-cup-betting-system-frontend.onrender.com/](https://world-cup-betting-system-frontend.onrender.com/)
- **Backend API (Swagger Docs):** [https://world-cup-betting-system.onrender.com/docs](https://world-cup-betting-system.onrender.com/docs)

> **Nota sobre a hospedagem (Render Free Tier):** Por estar hospedado na camada gratuita do Render, o servidor backend entra em modo de repouso (*sleep*) se ficar inativo. Caso o primeiro carregamento demore cerca de 30 a 50 segundos, aguarde enquanto o servidor reinicia automaticamente.

---

## Tabela de Conteúdos

- [Visão Geral e Destaques](#visão-geral-e-destaques)
- [Status do Projeto](#status-do-projeto)
- [Arquitetura](#arquitetura)
- [Stack Tecnológica](#stack-tecnológica)
- [Como Rodar o Projeto](#como-rodar-o-projeto)
- [Documentação da API](#documentação-da-api)
- [Fontes e Referências](#fontes-e-referências)

---

## Visão Geral e Destaques

- **Odds Dinâmicas**: cálculo das odds com base no volume e na distribuição dos palpites realizados pelos usuários.
- **Predição por ML**: modelo de Regressão Logística que utiliza estatísticas históricas dos times para estimar probabilidades de vitória, empate ou derrota.
- **Gerenciamento de Partidas**: administradores podem importar partidas, gerenciar competições e disponibilizar partidas para apostas.
- **Gerenciamento de Apostas**: usuários podem visualizar partidas disponíveis e realizar apostas de acordo com as regras do sistema.
- **Liquidação de Apostas**: processamento dos resultados das apostas após a finalização das partidas.
- **Relatórios e Estatísticas**: estatísticas de usuários, times e sistema, além da geração de relatórios em CSV.
- **Ranking**: sistema de pontuação e classificação dos usuários com base no desempenho nas apostas.
- **Autenticação e Autorização**: autenticação com JWT e controle de acesso baseado no perfil do usuário.

---

## Status do Projeto

| Funcionalidade | Descrição | Status |
|---|---|---|
| **Fundação & Banco** | Modelos SQLAlchemy, migrations Alembic e Docker Compose | Concluído |
| **Autenticação & Roles** | JWT, validação de idade (+18), perfil e controle de acesso administrativo | Concluído |
| **Partidas & Competições** | Importação via Football API, Copa do Mundo e Brasileirão | Concluído |
| **Disponibilidade para Apostas** | Administrador disponibiliza partidas para apostas | Concluído |
| **Apostas & Odds** | Regras de aposta, cálculo dinâmico de odds e multiplicação | Concluído |
| **Liquidação & Ranking** | Processamento de resultados, ranking e pontuação | Concluído |
| **Machine Learning** | Modelo de Regressão Logística para predição de partidas | Concluído |
| **Estatísticas & CSV** | Estatísticas de desempenho e exportação de relatórios em CSV | Concluído |
| **Documentação** | Docstrings, Swagger/ReDoc e exceptions globais | Concluído |
| **Frontend Web** | Interface em React + Vite | Concluído |

---

## Arquitetura

### Diagrama Lógico

![Diagrama Lógico](backend/docs/diagrama_logico.png)

### Diagrama Conceitual

![Diagrama Conceitual](backend/docs/diagrama_conceitual.png)

---

## Stack Tecnológica

### Backend

- **Linguagem:** Python 3.12+
- **Framework:** FastAPI + Uvicorn
- **Banco de Dados:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Validação:** Pydantic V2
- **Machine Learning:** Scikit-learn
- **Análise de dados:** Pandas
- **Persistência do modelo:** Joblib
- **Autenticação:** JWT
- **Criptografia de senha:** Bcrypt
- **Integrações HTTP:** HTTPX

### Frontend

- **Framework:** React + Vite
- **Roteamento:** React Router DOM
- **Comunicação HTTP:** Axios
- **Estilização:** CSS

### DevOps & Infraestrutura

- **Containers:** Docker
- **Orquestração:** Docker Compose

---

## Como Rodar o Projeto

O projeto pode ser executado com o banco de dados em Docker e o backend/frontend localmente.

### Pré-requisitos

- **Docker** e **Docker Compose**
- **Python 3.12+**
- **Node.js 18+**
- **npm**

---

## Executando o Backend

### 1. Acesse o diretório do backend

```bash
cd backend
```

### 2. Crie e ative o ambiente virtual

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na pasta `backend/`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/worldcup_db
SECRET_KEY=sua_chave_secreta
API_KEY=sua_chave_football_data_org
```

> **Importante:** não versione o arquivo `.env` no Git. Utilize um `.env.example` para documentar as variáveis necessárias.

### 5. Inicie o PostgreSQL

Na raiz do projeto:

```bash
docker compose up -d
```

### 6. Execute as migrations

Dentro do diretório `backend/`:

```bash
alembic upgrade head
```

### 7. Inicie o servidor

```bash
uvicorn app.main:app --reload
```

O backend estará disponível em:

```text
http://127.0.0.1:8000
```

---

## Executando o Frontend

Em outro terminal:

### 1. Acesse o diretório

```bash
cd frontend
```

### 2. Instale as dependências

```bash
npm install
```

### 3. Inicie o servidor

```bash
npm run dev
```

O frontend estará disponível em:

```text
http://localhost:5173
```

---

## Documentação da API

Com o backend em execução, a documentação interativa pode ser acessada através de:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

A API permite testar as operações diretamente pelo Swagger, incluindo autenticação, gerenciamento de usuários, partidas, apostas, estatísticas e predições.

---

## Machine Learning

O sistema possui um módulo de Machine Learning responsável por realizar predições de resultados de partidas.

O modelo utiliza dados históricos de partidas finalizadas armazenadas no PostgreSQL para gerar características relacionadas ao desempenho dos times, como:

- Média de gols marcados;
- Média de gols sofridos;
- Taxa de vitórias;
- Taxa de empates;
- Taxa de derrotas.

O modelo utilizado é uma **Regressão Logística (`LogisticRegression`)**, disponibilizada pelo Scikit-learn.

As predições são disponibilizadas através da API e retornam probabilidades para:

- Vitória do mandante;
- Empate;
- Vitória do visitante.

O modelo é persistido em arquivo binário utilizando Joblib.

---

## Estatísticas e Relatórios

O sistema possui um módulo de estatísticas responsável por consultar informações agregadas diretamente no banco de dados.

Entre as informações disponíveis estão:

### Estatísticas de partidas

- Total de apostas;
- Apostas em vitória do mandante;
- Apostas em vitória do visitante;
- Apostas em empate;
- Informações da partida.

### Estatísticas de usuários

- Total de apostas;
- Apostas pendentes;
- Apostas vencidas;
- Apostas perdidas;
- Apostas empatadas;
- Pontos investidos;
- Palpite mais utilizado;
- Time mais utilizado nos palpites.

### Estatísticas de times

- Partidas disputadas;
- Vitórias;
- Empates;
- Derrotas;
- Gols marcados;
- Gols sofridos.

### Relatórios

Os dados podem também ser exportados em formato CSV para análise externa.

O CSV funciona como **recurso de exportação**, não sendo utilizado como fonte de dados para o módulo de Machine Learning.

---

## Fluxo de Apostas

O sistema possui uma separação entre uma partida estar marcada para acontecer e estar disponível para apostas.

O fluxo é:

```text
Partida importada
       ↓
     TIMED
       ↓
Administrador disponibiliza
       ↓
is_bet_available = true
       ↓
Usuário visualiza partidas disponíveis
       ↓
Usuário realiza uma aposta
       ↓
Aposta PENDING
       ↓
Partida finalizada
       ↓
Liquidação da aposta
       ↓
WON / LOST / DRAW
```

Essa abordagem permite que o administrador controle quais partidas estão efetivamente disponíveis para os usuários realizarem apostas.

---

## Estrutura Simplificada

```text
world-cup-betting-system/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── services/
│   │
│   ├── alembic/
│   ├── ml_models/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## Fontes e Referências

### FastAPI

Hashtag Treinamentos - Curso de FastAPI:

https://www.youtube.com/playlist?list=PLpdAy0tYrnKy3TvpCT-x7kGqMQ5grk1Xq

Documentação oficial do FastAPI:

https://fastapi.tiangolo.com/

Query Parameters e validações:

https://fastapi.tiangolo.com/tutorial/query-params-str-validations/

### SQLAlchemy

Documentação oficial do SQLAlchemy:

https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html

### Scikit-learn

Documentação oficial do Scikit-learn:

https://scikit-learn.org/

https://medium.com/@msremigio/regress%C3%A3o-log%C3%ADstica-logistic-regression-997c6259ff9a

### Pydantic

Documentação oficial do Pydantic:

https://docs.pydantic.dev/

### PostgreSQL

Documentação oficial do PostgreSQL:

https://www.postgresql.org/docs/

### Padrões de Código e Documentação

O projeto utiliza como referência o **Google Python Style Guide**, especialmente as recomendações relacionadas a comentários e docstrings:

https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings

---
