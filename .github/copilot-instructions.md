## Resumo rápido

Este repositório (monorepo) provê um backend FastAPI (agentes), um frontend React (PWA) e um scaffold para integração com um LLM local (Ollama). Os agentes atuam como micro-serviços lógicos (pesquisa, redator jurídco, métricas) e usam RAG/embeddings a partir de arquivos em `docs/`.

## Objetivo para um agente AI (Copilot/assistente)
- Entender o fluxo: `requests -> backend/agents.py (schema_for/run_agent) -> backend/llm.py + backend/rag.py -> retorno`.
- Preservar contratos: as respostas de `POST /agents/{agent}/run` devem validar para `backend/models.py::AgentRunResponse`.
- Ao alterar a lógica de um agente, atualize `docs/agents.md` e adicione/ajuste testes em `backend/tests/`.

## Comandos comuns (execução local)
- Rodar Ollama (requerido para LLM local):
  - `brew install ollama` (macOS)
  - `ollama serve` e `ollama pull mistral`
- Backend (local):
  - `cd backend`
  - `python -m venv .venv && source .venv/bin/activate`
  - `pip install -r requirements.txt`
  - `uvicorn backend.main:app --reload --port 8000`
- Frontend:
  - `cd frontend && npm install && npm run dev` (http://localhost:3000)
- Docker (recomendado para evitar builds nativos):
  - `docker compose up --build`

## Arquivos e padrões-chave
- `backend/agents.py`: lista/registro de agentes e função `run_agent` simples; ao implementar agente real, chamar `llm.generate()` e `rag.retrieve()` a partir daqui.
- `backend/llm.py`: cliente LLM com integração para Ollama e fallback mock. Use `LLMClient.generate(prompt, ...)` para chamadas de modelo.
- `backend/rag.py`: leitor simples que indexa `docs/`. Para aumentar precisão, substituir por armazenamentos vetoriais (FAISS/Milvus) e embeddings (`backend/embeddings.py`).
- `backend/models.py`: pydantic para `AgentRunRequest` e `AgentRunResponse` — alterar só se for realmente necessário e garantir compatibilidade.
- `backend/db/`: modelos SQLAlchemy (`models.py`), sessão (`session.py`), alembic para migrações (`alembic/`).
- `docs/agents.md`: especificação de agentes — sincronizar com mudanças em `agents.py`.

## Integrações e requisitos externos
- LLM local: Ollama por padrão; a variável `LLM_PROVIDER` pode ser alterada para `openai` etc., com `LLM_API_KEY`.
- RAG/Embeddings: `sentence-transformers` opcional — fallback hashing já implementado.
- Banco: `DATABASE_URL` no `.env` (padrão sqlite). Alembic existe para migrações;
- Autenticação: `backend/auth.py` usa JWT; atualizar `SECRET_KEY` em produção.

## Convenções e dicas de implementação
- Sempre mantenha a resposta compatível com `AgentRunResponse` (pydantic) para evitar discrepâncias de schema nas rotas.
- Encapsule chamadas externas (DataJud, CNJ, Judit) em `backend/adapters/` e torne-as “pluggable”.
- Para novos agentes:
  1. Adicione definição em `AGENTS` (backend/agents.py).
  2. Adicione implementação em `run_agent` ou crie um handler separado que use `llm.generate()` + `rag.retrieve()`.
  3. Atualize `docs/agents.md` com schema e permissões (RBAC).
  4. Adicione ou atualize testes em `backend/tests/`.
- Uso do DB: prefira `SessionLocal()` com `try/finally` para fechar a sessão (ex.: `get_space_kpis`).

## Testes e validação rápida
- Backend: `bash backend/test.sh` (verifica Ollama + endpoints/agents básicos).
- Unit tests: `pytest` em `backend/tests/`.
- Lint/format: siga o padrão do repo (use `black`/`flake8` se configurado).

## Observações de segurança/produção
- Nunca deixar `SECRET_KEY` default em produção. Use `DATABASE_URL` e variáveis de ambiente seguras.
- Persistir trilha de auditoria (`backend/db/models.py::AuditLog`) para qualquer execução de agente.
- As chamadas do agente devem retornar referências de fonte quando aplicável (RAG) e `confidence_score`.

## Onde começar para tarefas comuns
- Implementar LLM real para `redator`: editar `backend/agents.py` -> chamar `backend/rag.retrieve()` -> criar prompt baseado em `docs/agents.md` -> `backend/llm.generate()`. Atualizar testes.
- Adicionar nova rota para metadata: editar `backend/main.py` e adicionar validação com `backend/auth.py`.

**Exemplo rápido (pseudo-código)**
```python
# backend/agents.py (simplificado)
from backend.rag import retrieve
from backend.llm import generate

def run_agent(agent, payload):
  if agent == 'redator':
    ctx = payload.get('input', '')
    docs = retrieve(ctx, top_k=3)
    prompt = f"{ctx}\n\nContexto recuperado:\n" + '\n'.join([d['snippet'] for d in docs])
    out = generate(prompt, max_tokens=1024)
    return { 'title': 'Rascunho', 'sections': [{ 'name': 'Principal', 'text': out['text']}], 'confidence_score': 0.8 }
```

## Perguntas de follow-up
- Deseja que eu adicione exemplos de patchs (template PR) para alterações nos agentes, ou que eu crie um checklist de revisão de segurança para execuções de agentes?

---
Atualize e ajuste com feedback; mantenho `docs/agents.md` como fonte da verdade para prompts e contratos.
