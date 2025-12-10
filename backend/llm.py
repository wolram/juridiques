import os
from typing import Any, Dict
import requests
import logging

logger = logging.getLogger(__name__)


class LLMClient:
    """LLM client com suporte a Ollama (gratuito, local) e fallback para mock."""

    def __init__(self, provider: str = None, api_key: str = None, ollama_url: str = None):
        self.provider = provider or os.getenv("LLM_PROVIDER", "ollama")
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.ollama_url = ollama_url or os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = os.getenv("LLM_MODEL", "mistral")  # Padrão: Mistral (open-source)

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> Dict[str, Any]:
        if self.provider == "ollama":
            return self._generate_ollama(prompt, max_tokens, temperature)
        # Fallback: mock
        logger.warning("LLM Provider '%s' não configurado. Retornando mock.", self.provider)
        return {"text": f"[MOCK LLM] Resposta para prompt (len={len(prompt)}):\n{prompt[:200]}", "usage": {"tokens": 10}}

    def _generate_ollama(self, prompt: str, max_tokens: int, temperature: float) -> Dict[str, Any]:
        """Chamar Ollama via HTTP (requer Ollama rodando em localhost:11434)."""
        try:
            resp = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": temperature,
                },
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "text": data.get("response", ""),
                "usage": {"tokens": data.get("eval_count", 0)},
            }
        except Exception as e:
            logger.error("Falha ao chamar Ollama: %s. Retornando mock.", e)
            return {"text": f"[MOCK - Ollama indisponível] Resposta truncada.", "usage": {"tokens": 0}}


default_client = LLMClient()


def generate(prompt: str, **kwargs) -> Dict[str, Any]:
    return default_client.generate(prompt, **kwargs)
