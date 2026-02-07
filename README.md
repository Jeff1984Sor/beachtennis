# Beach Tennis School

Projeto completo para gestão de escola de Beach Tennis com backend FastAPI + Postgres e app mobile único (Expo) com experiência por perfil: gestor, professor e aluno.

## Estrutura
- `backend/`: API FastAPI (auth JWT, agenda, alunos, comissões, contratos, mídia, DRE)
- `mobile/`: app React Native (Expo Router + React Query + RHF + Zod)
- `docker-compose.yml`: Postgres + backend

## Subir backend com Docker
```bash
cd C:\Users\JeffersonFernandes\Projetos\Beachetenis_final
docker compose up --build
```

Backend em `http://localhost:8000`.

## Rodar migrações e seeds
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python -m app.seeds.seed
```

## Rodar app mobile
```bash
cd mobile
npm install
npm run start
```

Defina a API no Expo se necessário:
```bash
set EXPO_PUBLIC_API_URL=http://localhost:8000
```

## Usuários seed
- Gestor
- email: `gestor@local`
- senha: `gestor123`

- Professor
- email: `professor@local`
- senha: `professor123`

- Aluno
- email: `aluno@local`
- senha: `aluno123`

## Fluxos do app mobile
1. Login único com branding público (`/public/branding`).
2. Após login o app chama `/auth/me`, identifica papéis e monta abas por perfil.
3. Menu "Trocar visão" permite alternar entre papéis disponíveis no mesmo usuário.
4. Agenda do dia com cards, filtros e ações rápidas (confirmar, realizada, cancelar).
5. Alunos com ficha completa: Aulas, Financeiro, WhatsApp, Contrato e Anexos (upload + abrir).
6. Financeiro:
- gestor: receber/pagar
- professor: comissões (visão pagar)
- aluno: receber próprio
7. Configurações gestor: geração de comissão do mês anterior e busca CEP.

## Endpoints usados no mobile
- `POST /auth/login`
- `POST /auth/refresh`
- `GET /auth/me`
- `GET /public/branding`
- `GET /mobile/agenda-dia`
- `GET /mobile/alunos`
- `GET /mobile/alunos/{id}/ficha`
- `GET /mobile/financeiro`
- `GET /alunos/{id}/anexos`
- `POST /alunos/{id}/anexos/upload`
- `PUT /agenda/aulas/{id}`
- `POST /comissoes/gerar`
- `GET /utils/cep/{cep}`
- `GET /financeiro/dre`

## Observações
- Uploads são salvos em filesystem (`/media` no container).
- O backend mantém endpoints existentes e adiciona camada `/mobile` para payloads otimizados para app.
