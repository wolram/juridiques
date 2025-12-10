# Backend com Ollama (LLM local gratuito)

## Antes de começar: Instalar e rodar Ollama

[Ollama](https://ollama.ai) é um motor LLM de código aberto que roda localmente. Suportamos `Mistral` (7B) e `Llama2` (7B/13B) como padrão.

### 1. Instalar Ollama:
```bash
# macOS (via Homebrew)
brew install ollama

# ou Linux
curl https://ollama.ai/install.sh | sh

# ou Windows: https://ollama.ai/download
```

### 2. Rodar Ollama em background:
```bash
ollama serve
```

### 3. Fazer download do modelo (em outro terminal):
```bash
# Mistral (recomendado, ~4GB, muito rápido)
ollama pull mistral

# ou Llama2 (7B, ~4GB)
ollama pull llama2

# ou Neural Chat (7B, especializado)
ollama pull neural-chat
```

Ollama estará pronto em `http://localhost:11434` por padrão.

## Executar o backend com Ollama

```bash
# 1. Criar venv e instalar dependências
cd /Users/marlow/APP/juridiques
cp .env.example .env

# Use Python 3.11 ou 3.10. Se der erro na instalação de pydantic-core, prefira executar via Docker.
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt || echo "Se houver falha ao compilar dependências nativas, use Docker."

# 2. Iniciar Ollama (em outro terminal, se ainda não estiver)
ollama serve

# 3. Em um terceiro terminal, rodar o backend
source .venv/bin/activate
uvicorn backend.main:app --reload --port 8000
```

Teste a API: abra `http://localhost:8000/docs`

Endpoints principais:
- `GET /agents` — listar agentes
- `POST /agents/redator/run` — gerar rascunho de peça
- `POST /agents/pesquisa/run` — buscar processos/jurisprudência
- `POST /agents/metrics/run` — calcular KPIs

## Configurações via `.env`

```
LLM_PROVIDER=ollama
LLM_MODEL=mistral    # ou llama2, neural-chat, etc.
OLLAMA_URL=http://localhost:11434
```

Se quiser usar outro modelo, basta trocar `LLM_MODEL` e garantir que rodou `ollama pull <modelo>`.

## Performance e ajustes

- **Mistral 7B**: rápido, ~3-5s por prompt (recomendado para produção local)
- **Llama2 7B**: similar ao Mistral
- **Neural Chat 7B**: otimizado para bate-papo
- Para testar rapidamente: `ollama pull tinyllama` (~600MB)

Se Ollama não estiver disponível, o backend cai automaticamente para mock (respostas truncadas).
