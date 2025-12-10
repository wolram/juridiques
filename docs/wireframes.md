# Wireframes - Telas Principais (exemplo)

```mermaid
flowchart TB
  subgraph Main
    ChatPane["Chat central\n- Marca (logo)\n- Histórico de mensagens\n- Referências de fontes"]
    SideBar["Lateral\n- Avatar usuário\n- Lista de threads\n- Filtros (espaço, cliente, tribunal)"]
    Bottom["Input\n- Campo de texto\n- Upload arquivos\n- Seleção de modo/modelo\n- Botão enviar (nova thread)"]
  end

  SideBar --> ChatPane
  ChatPane --> Bottom

  class ChatPane,SideBar,Bottom fill:#fff,stroke:#333
```

Notas rápidas:
- O `ChatPane` exibe referência de fonte abaixo de cada mensagem (ex.: DataJud, STJ, legislação).
- O `Bottom` permite upload múltiplo, seleção de `modo` (consulta / rascunho / resumo) e quick-settings (idioma, formalidade).
- Ao clicar no `avatar`, abre painel de perfil e configurações (OAB, integrações, keys).
