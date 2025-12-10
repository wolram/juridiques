# Agentes - Especificação

Este documento descreve os três agentes iniciais (personas) do produto jurídico de IA: `Pesquisa`, `Redator Jurídico` e `Gestor de Métricas`.

## Visão Geral

- Cada agente atua como um micro-serviço lógico com responsabilidades, permissões e prompts próprios.
- Os agentes podem ser invocados via endpoint REST e integrados ao fluxo de `threads` e `espaços`.
- Saídas devem sempre incluir referências (fontes) quando aplicável e metadados de confiança.

## Agent 1: Pesquisa

- Propósito: localizar processos, decisões e jurisprudência relevantes; enriquecer threads com metadados processuais.
- Entradas: texto de consulta, número CNJ, filtros (tribunal, data, tipo de documento).
- Saídas: lista ranqueada de resultados (título, tribunal, data, trecho relevante, link/fonte, score de relevância).
- Permissões: leitura de bases externas (DataJud/CNJ/Judit), leitura de índice local de documentos.
- Prompt base (template):

```
Você é o Agente Pesquisa — especialista em buscas processuais e jurisprudência. Dado o input do usuário e filtros, retorne até N resultados relevantes ordenados por relevância. Para cada resultado, inclua: título, tribunal, data, resumo de 1-2 linhas, trecho citado (contexto), fonte (DataJud/CNJ/Judit ou interno) e score.
Se o input contiver número de processo CNJ, tente recuperar metadados estruturados e indique se há correspondência exata.
```

## Agent 2: Redator Jurídico

- Propósito: gerar rascunhos de peças, resumos, minutas e sugestões de parágrafos com citações normativas.
- Entradas: contexto do caso (thread), documentos anexados, modelo/estilo (formalidade, idioma), tipo de peça.
- Saídas: rascunho estruturado em seções (preâmbulo, fatos, fundamentos jurídicos, pedido), com citações / referências e sugestões de anexos.
- Permissões: leitura de thread e documentos; escrita de rascunhos em thread; acesso ao histórico de modelos de peças.
- Prompt base (template):

```
Você é o Redator Jurídico — redija um rascunho de {tipo_de_peca} usando o contexto abaixo. Adote tom {formalidade}. Cite normas e decisões relevantes, indicando fonte e link quando possível. Marque claramente trechos sugeridos e trechos que exigem validação humana (ex.: cálculos, datas). Entregue saída em JSON: {title, sections:[{name, text, citations:[{type, ref, link}]}], confidence_score}.
```

## Agent 3: Gestor de Métricas

- Propósito: calcular e expor KPIs por `espaço` ou por usuário, gerar alertas (prazos, SLA) e responder consultas sobre métricas.
- Entradas: comando de consulta (ex.: "KPIs do espaço X, últimos 30 dias"), parâmetros de filtro.
- Saídas: painel de métricas resumidas (volume, taxa de sucesso, prazos perdidos, tempo médio de resposta) e séries temporais para gráficos.
- Permissões: leitura de metadados processuais, leitura de threads e estado; geração de relatórios exportáveis; não permite edição de peças.
- Prompt base (template):

```
Você é o Gestor de Métricas — calcule os KPIs solicitados a partir dos dados disponíveis para o escopo: {espaço|cliente|período}. Retorne métricas-chave e, quando relevante, uma explicação curta da metodologia (ex.: como foi calculada a taxa de sucesso). Indique fontes dos dados e se há dados faltantes.
```

## Integração / Endpoints sugeridos

- `GET /agents` — lista agentes e capacidades.
- `POST /agents/{agent}/run` — executa um agente com payload JSON: `{input, thread_id?, space_id?, user_id?, options?}`.
- `GET /agents/{agent}/schema` — retorna schema de entrada/saída e scopes necessários.

## RBAC e Segurança

- Cada agente define scopes mínimos: `agent:pesquisa:read`, `agent:redator:write`, `agent:metrics:read`.
- Todas as chamadas devem ser auditadas (quem, quando, input hash) e armazenadas com trilha de decisão para conformidade.

## Observações de implementação

- Use RAG (retrieval-augmented generation) para o `Redator Jurídico`: recuperar documentos/trechos e passar ao modelo como contexto.
- Cachear resultados de pesquisa por 24h com validade baseada em assinatura e fonte.
- Outputs com probabilidades/`confidence_score` e marcação de conteúdo que precisa de validação humana.
