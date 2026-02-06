# Beach Tennis School

Repositório completo para gestão de uma escola de Beach Tennis: FastAPI + Postgres, Admin Web (Next.js) e Mobile (Expo).

## Stack
- Backend: FastAPI, SQLAlchemy 2.0 async, Alembic, Pydantic v2
- DB: Postgres
- Frontend Admin: Next.js + TypeScript
- Mobile: React Native (Expo) + TypeScript

## Como rodar (backend)
```bash
cd backend
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```

Crie `.env` a partir de `.env.example`.

Rodar com Docker Compose:
```bash
cd ..
docker compose up --build
```

### Migrations
```bash
cd backend
alembic revision --autogenerate -m "init"
alembic upgrade head
```

### Seeds
```bash
cd backend
python -m app.seeds.seed
```

Credenciais padrão:
- email: `admin@local`
- senha: `admin123`

## Admin Web
```bash
cd admin-web
npm install
npm run dev
```

A UI já consome `/public/branding`.

## Mobile (Expo)
```bash
cd mobile
npm install
npm run start
```

## Endpoints principais
- `POST /auth/login`
- `POST /auth/refresh`
- `GET /public/branding`
- `GET /public/logo`
- `GET /utils/cep/{cep}`
- `POST /media/upload`
- `GET /media/{id}`
- `DELETE /media/{id}`
- `CRUD /alunos`
- `GET /alunos/{id}/ficha`
- `GET /alunos/{id}/anexos`
- `POST /alunos/{id}/anexos/upload`
- `CRUD /unidades`
- `CRUD /planos`
- `CRUD /profissionais`
- `CRUD /contratos`
- `CRUD /regras-comissao`
- `POST /comissoes/gerar?unidade_id=&mes=YYYY-MM`
- `GET /financeiro/dre?unidade_id=&inicio=YYYY-MM-DD&fim=YYYY-MM-DD&modo=caixa|competencia`

## Observações
- Uploads ficam em `MEDIA_ROOT` por ano/mês e preservam extensão.
- Branding e logo são públicos via endpoints.
- RBAC via `PerfilAcesso.permissoes` (JSON).

## Próximos passos
- Completar validações de agenda e capacidade.
- Implementar editor de contratos e variáveis no admin-web.
- Implementar telas e autenticação no mobile.