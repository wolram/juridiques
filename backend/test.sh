#!/bin/bash

# Script para testar o backend com Ollama

set -e

echo "=== Juridiques Backend Test ==="
echo

# Verificar se Ollama está rodando
echo "1. Verificando Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama está rodando"
else
    echo "✗ Ollama não encontrado em http://localhost:11434"
    echo "   Execute em outro terminal: ollama serve"
    exit 1
fi

echo
echo "2. Testando endpoint /agents..."
curl -s http://localhost:8000/agents | python3 -m json.tool

echo
echo "3. Testando agent 'redator' (gerar rascunho)..."
curl -s -X POST http://localhost:8000/agents/redator/run \
  -H "Content-Type: application/json" \
  -d '{"input": "Preciso de um rascunho de contestação para ação de cobrança"}' | python3 -m json.tool

echo
echo "✓ Tests completos!"
