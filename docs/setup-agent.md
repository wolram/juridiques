setup-agent
## Mapeamento dos agentes por frente

- orquestrador_backend
  - Função: DB, auth, RBAC, auditoria, migrations, Docker/CI.
  - Permissões: db:manage, auth:manage, deploy:orchestrate, audit:log
  - Uso: comandos administrativos, geração de migrations, scripts de seed, runbooks de deploy.

- designer_frontend
  - Função: UI/UX, componentes React/PWA, chat, upload, dashboard.
  - Permissões: ui:design, frontend:build, pwa:offline
  - Uso: criar/alterar componentes, wireframes, testes visuais e acessibilidade.

- integrador_llm_rag
  - Função: integração de modelos (Ollama), embeddings, RAG e adaptadores DataJud/CNJ/Judit.
  - Permissões: llm:invoke, vecstore:manage, adapter:external
  - Uso: indexação de documentos, buscas semânticas, fallback de embeddings e endpoints de inference.

## Como invocar
Endpoints expostos (mock) no backend:
- GET /agents -> lista agentes
- GET /agents/{agent_id}/schema -> retorno do schema do agente
- POST /agents/{agent_id}/run -> executa ação (payload JSON)

# ...existing code...