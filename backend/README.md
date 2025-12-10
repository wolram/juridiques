# Backend scaffold (agents)

Rápido scaffold para testar os 3 agentes (Pesquisa, Redator Jurídico, Gestor de Métricas).

Execução local:

```bash
# usando venv local
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000

# ou com Docker (recomendado para evitar builds nativos de pydantic-core)
docker compose up --build
# abra http://localhost:8000/docs
```

Endpoints:

- `GET /agents` — lista agentes
- `GET /agents/{agent}/schema` — schema simples
- `POST /agents/{agent}/run` — executa o agente (payload JSON)

Observações: este scaffold retorna respostas mockadas e templates. Substituir integração com provedores de LLM e DataJud/CNJ/Judit conforme necessário.

Próximos passos implementados neste scaffold:
- `backend/llm.py` - cliente LLM stub
- `backend/rag.py` - retriever simples baseado em arquivos de `docs/`
- `backend/embeddings.py` - embeddings com `sentence-transformers` opcional e fallback
- `backend/adapters/datajud.py` - adaptador stub para DataJud/CNJ

