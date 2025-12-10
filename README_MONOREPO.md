# Monorepo - Juridiques

Assistente jurídico de IA multi-plataforma (web, desktop, mobile).

## Estrutura

```
juridiques/
├── backend/               # API FastAPI + Ollama + DB
│   ├── main.py           # Servidor principal
│   ├── agents.py         # Agentes (Pesquisa, Redator, Métricas)
│   ├── auth.py           # JWT + RBAC
│   ├── audit.py          # Logging de auditoria
│   ├── llm.py            # Cliente Ollama
│   ├── rag.py            # Retriever
│   ├── embeddings.py     # Embeddings local/fallback
│   ├── db/
│   │   └── models.py     # SQLAlchemy models
│   ├── adapters/
│   │   └── datajud.py    # DataJud/CNJ stub
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── README_OLLAMA.md
│   └── test.sh
│
├── frontend/              # React + PWA
│   ├── src/
│   │   ├── components/    # MainLayout, ChatPanel, ThreadSidebar
│   │   ├── store/         # Zustand (chatStore)
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── public/
│   │   ├── manifest.json
│   │   ├── sw.js          # Service Worker
│   │   └── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── docs/
│   ├── agents.md          # Especificação dos agentes
│   ├── architecture.md    # Diagrama de arquitetura
│   └── wireframes.md      # Wireframes das telas
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## Início rápido

### 1. Backend + Ollama (LLM local)

```bash
# Instalar Ollama (macOS)
brew install ollama
ollama serve  # em um terminal

# Em outro terminal, rodar Ollama pull
ollama pull mistral

# Setup backend
cd backend
cp ../.env.example ../.env
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Testes
bash test.sh
```

### 2. Frontend (React + PWA)

```bash
# Instalar dependências
cd frontend
npm install

# Rodar dev server
npm run dev
# Acessa em http://localhost:3000

# Buildar para produção
npm run build
```

### 3. Docker (recomendado)

```bash
# Na raiz do projeto
docker compose up --build
# Backend em http://localhost:8000
# Frontend em http://localhost:3000 (build necessário)
```

## Features implementadas

✅ 3 Agentes (Pesquisa, Redator Jurídico, Gestor de Métricas)
✅ Ollama LLM integrado (gratuito, local)
✅ RAG + Embeddings (com fallback)
✅ Adaptadores DataJud/CNJ (stubs)
✅ Autenticação JWT + RBAC
✅ Logging de auditoria
✅ Frontend React com PWA (chat, threads, sidebar)
✅ Tailwind CSS + componentes responsivos
✅ Service Worker para offline
✅ Vite para build otimizado

## Próximas etapas

- [ ] Integração com provedores reais (DataJud/CNJ/Judit)
- [ ] Banco de dados (PostgreSQL) + migrations
- [ ] Testes unitários e E2E
- [ ] Deploy (Azure, Vercel, etc.)
- [ ] Mobile (Electron + Capacitor)
- [ ] Dashboards e KPIs
- [ ] Exportação de peças (PDF/Word)
