# Arquitetura - Visão Geral

```mermaid
flowchart LR
  subgraph Frontend
    A[Web App (React/PWA)]
    B[Desktop (Electron)]
    C[Mobile (PWA/Capacitor)]
  end

  subgraph Backend
    D[API Gateway / FastAPI]
    E[Auth / RBAC]
    F[Agents Service]
    G[RAG Service]
    H[Adapters (DataJud, CNJ, Judit)]
    I[Vector Store / Embeddings]
    J[DB (Postgres) & Audit Log]
  end

  A --> D
  B --> D
  C --> D
  D --> E
  D --> F
  F --> G
  G --> I
  G --> H
  H --> |external APIs| External[DataJud/CNJ/Judit]
  F --> J
  E --> J

  classDef infra fill:#f9f,stroke:#333,stroke-width:1px;
  class External infra
```

Explicação rápida:
- `Frontend`: app principal (PWA) que também é empacotado como Electron para desktop.
- `Backend`: FastAPI serve endpoints REST/GraphQL; `Agents Service` orquestra chamadas aos agentes; `RAG Service` lida com recuperação de documentos e vetorização; `Adapters` encapsulam integrações com DataJud/CNJ/Judit.
- `Vector Store`: pode ser FAISS, Milvus ou serviço gerenciado; embeddings via OpenAI/Local models.
- `DB`: armazena `threads`, `espacos`, `processos`, `KPIs`, permissões e trilhas de auditoria.

Segurança e conformidade: TLS, criptografia at-rest para dados sensíveis, registro de auditoria por ação do agente.
