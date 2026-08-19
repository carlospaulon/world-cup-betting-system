# PalpiteCopa — Frontend

Interface web em React + Vite para o World Cup Betting System (Copa do Mundo 2026). Consome a API FastAPI já desenvolvida (autenticação JWT, partidas, apostas, ranking, estatísticas e relatórios).

## Stack

- React 18 + Vite
- React Router 6 (rotas protegidas por autenticação e por papel de admin)
- Axios (cliente HTTP com interceptor de JWT)
- CSS puro com design tokens (sem framework de UI)

## Como rodar

1. Instale as dependências:
   ```bash
   npm install
   ```
2. Copie o arquivo de ambiente e ajuste a URL da API se necessário:
   ```bash
   cp .env.example .env
   ```
   O padrão já aponta para `http://127.0.0.1:8000`, onde o backend roda localmente.
3. Suba o backend (FastAPI + PostgreSQL via Docker) normalmente, conforme o README do backend.
4. Rode o frontend:
   ```bash
   npm run dev
   ```
5. Acesse `http://localhost:5173`.

## Build de produção

```bash
npm run build
npm run preview
```

## Estrutura

```
src/
├── api/client.js          → todas as chamadas HTTP para o backend
├── context/                → AuthContext (usuário logado) e ToastContext (notificações)
├── components/
│   ├── layout/              → Navbar e guards de rota (ProtectedRoute, AdminRoute, GuestRoute)
│   ├── ui/                  → Loading, EmptyState
│   └── MatchTicket.jsx      → card de partida com odds e formulário de aposta
├── pages/                   → uma página por rota
│   └── admin/                → área exclusiva de administrador
├── utils/format.js          → labels de enums (prediction, status) e formatação de data
└── styles/                  → tokens de design e folha de estilos principal
```

## Fluxo de autenticação

O login usa `OAuth2PasswordRequestForm` no backend (necessário para o Swagger funcionar), então o frontend envia `username`/`password` como `application/x-www-form-urlencoded`, mesmo a UI mostrando um campo "E-mail". O token JWT é salvo em `localStorage` e anexado automaticamente em toda requisição via interceptor do Axios.

## Papéis de usuário

- **Usuário comum**: vê e aposta em partidas abertas, acompanha suas apostas, ranking, retrospecto de seleções e o próprio perfil.
- **Administrador** (`is_admin: true`): tudo o que o usuário comum vê, mais a área `/admin` — importar partidas da API externa, finalizar partidas (liquidando apostas automaticamente), gerenciar usuários (promover a admin, buscar por CPF) e baixar relatórios CSV.

Não há tela de "virar admin" pelo cadastro — a promoção acontece via `PATCH /users/admin/{user_id}/role`, disponível apenas para quem já é admin.
