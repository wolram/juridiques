from typing import Optional, Dict


def fetch_process_by_cnj(cnj: str) -> Optional[Dict[str, str]]:
    """Stub para buscar metadados de processo por número CNJ.

    Substituir por chamada real à API do DataJud/CNJ com autenticação e tratamento de erros.
    """
    # Mocked example
    if not cnj:
        return None
    return {
        "cnj": cnj,
        "tribunal": "TRF1",
        "classe": "Ação Ordinária",
        "partes": "Fulano de Tal x Sicrano",
        "status": "Em andamento",
    }
