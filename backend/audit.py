# Logging de auditoria

from datetime import datetime
from typing import Optional, Any
import json
import logging

logger = logging.getLogger(__name__)


class AuditLogger:
    """Registra ações de usuários para conformidade e segurança."""
    
    def __init__(self, db_session=None):
        self.db_session = db_session
    
    def log_action(
        self,
        user_id: int,
        action: str,
        resource_type: str,
        resource_id: Optional[int] = None,
        details: Optional[dict] = None,
    ):
        """Log uma ação realizada por um usuário."""
        from backend.db.models import AuditLog
        
        audit_entry = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            created_at=datetime.utcnow(),
        )
        
        if self.db_session:
            self.db_session.add(audit_entry)
            self.db_session.commit()
        
        # Também logar em arquivo/stdout para auditoria em tempo real
        logger.info(
            f"AUDIT: user_id={user_id} action={action} resource={resource_type}#{resource_id} details={json.dumps(details)}"
        )


# Instância global de auditoria
audit = AuditLogger()
