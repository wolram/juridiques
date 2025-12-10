from typing import Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
from backend.db import models


def compute_kpis_for_space(db: Session, space_id: int) -> Dict[str, Any]:
    # Volume de processos
    volume = db.query(models.Process).filter(models.Process.space_id == space_id).count()

    # Taxa de sucesso (exemplo: processos com status 'concluded' / total)
    concluded = db.query(models.Process).filter(models.Process.space_id == space_id, models.Process.status == 'concluded').count()
    taxa_sucesso = (concluded / volume) if volume > 0 else None

    # Prazos perdidos: exemplo simplificado (campo não modelado) - retornamos 0 por enquanto
    prazos_perdidos = 0

    # Tempo médio de resposta: média entre created_at de thread e primeiro message
    from sqlalchemy import func
    avg_response = None
    q = (
        db.query(func.avg(func.julianday(models.Message.created_at) - func.julianday(models.Thread.created_at)))
        .join(models.Thread, models.Message.thread_id == models.Thread.id)
        .join(models.Space, models.Thread.space_id == models.Space.id)
        .filter(models.Space.id == space_id)
    )
    try:
        delta_days = q.scalar()
        if delta_days is not None:
            avg_response = float(delta_days) * 24 * 3600  # seconds
    except Exception:
        avg_response = None

    return {
        "volume": volume,
        "taxa_sucesso": taxa_sucesso,
        "prazos_perdidos": prazos_perdidos,
        "avg_response_seconds": avg_response,
        "as_of": datetime.utcnow().isoformat(),
    }
