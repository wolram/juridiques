from typing import Dict, Any

AGENTS = {
    "pesquisa": {
        "name": "Pesquisa",
        "scopes": ["agent:pesquisa:read"],
        "description": "Busca processos, decisões e jurisprudência.",
    },
    "redator": {
        "name": "Redator Jurídico",
        "scopes": ["agent:redator:write"],
        "description": "Gera rascunhos de peças com citações e fontes.",
    },
    "metrics": {
        "name": "Gestor de Métricas",
        "scopes": ["agent:metrics:read"],
        "description": "Calcula KPIs e gera relatórios por espaço/cliente.",
    },
}


def get_agents():
    return AGENTS


def schema_for(agent: str) -> Dict[str, Any]:
    if agent not in AGENTS:
        return {"error": "agent not found"}
    # Schema mínimo e ilustrativo
    return {
        "name": AGENTS[agent]["name"],
        "scopes": AGENTS[agent]["scopes"],
        "input_schema": {"input": "string", "thread_id": "string?", "options": "object?"},
        "output_hint": "Ver docs/agents.md para estrutura detalhada",
    }


def run_agent(agent: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    # Resposta mockada usando templates simples. Substituir por integração LLM + RAG.
    if agent == "pesquisa":
        q = payload.get("input", "")
        return {
            "results": [
                {"title": f"Resultado de teste para: {q}", "tribunal": "TRF1", "date": "2024-01-01", "snippet": "Trecho relevante...", "source": "DataJud", "score": 0.87}
            ]
        }
    if agent == "redator":
        ctx = payload.get("input", "")
        return {
            "title": "Rascunho gerado",
            "sections": [
                {"name": "Preâmbulo", "text": f"Preâmbulo baseado no contexto: {ctx}", "citations": []},
                {"name": "Fundamentos", "text": "Fundamentos jurídicos (exemplo)", "citations": [{"type": "lei", "ref": "Art. X", "link": None}]},
            ],
            "confidence_score": 0.78,
        }
    if agent == "metrics":
        return {"metrics": {"volume": 123, "taxa_sucesso": 0.42, "prazos_perdidos": 2}}
    return {"error": "agent not implemented"}
