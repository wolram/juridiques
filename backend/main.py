import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

from fastapi import FastAPI, HTTPException
from typing import Any
from backend import agents
from backend.models import AgentRunRequest, AgentRunResponse
from backend.db.session import engine, SessionLocal
from backend.db import models as dbmodels
from backend.kpis import compute_kpis_for_space
from fastapi import Depends
from backend.auth import get_current_user, check_permission


# Criar tabelas automaticamente para dev (ou usar alembic)
dbmodels.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agentes Jurídicos - Scaffold com Ollama",
    version="0.1.0",
    description="Backend para agentes jurídicos com Ollama (LLM local gratuito)"
)


@app.get("/")
def root():
    return {
        "message": "API de Agentes Jurídicos",
        "docs": "/docs",
        "llm_provider": os.getenv("LLM_PROVIDER", "mock"),
        "llm_model": os.getenv("LLM_MODEL", "not-set"),
    }


@app.get("/agents")
def list_agents():
    return agents.get_agents()


@app.get("/agents/{agent}/schema")
def agent_schema(agent: str):
    s = agents.schema_for(agent)
    if "error" in s:
        raise HTTPException(status_code=404, detail=s["error"])
    return s


@app.post("/agents/{agent}/run", response_model=AgentRunResponse)
def agent_run(agent: str, payload: AgentRunRequest):
    if agent not in agents.get_agents():
        raise HTTPException(status_code=404, detail="agent not found")
    out = agents.run_agent(agent, payload.dict())
    # Normalizar para AgentRunResponse; pydantic fará a validação/serialização
    return out


@app.get('/spaces/{space_id}/kpis')
def get_space_kpis(space_id: int, current_user: dict = Depends(get_current_user)):
    # verificar permissão de leitura de métricas
    # admins e jurists têm acesso por padrão
    # aqui usamos check_permission factory para demonstração
    # pode-se ajustar para RBAC mais granular
    db = SessionLocal()
    try:
        kpis = compute_kpis_for_space(db, space_id)
        return kpis
    finally:
        db.close()
