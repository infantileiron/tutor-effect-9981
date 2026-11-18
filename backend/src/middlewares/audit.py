from datetime import datetime,timezone
from starlette.middleware.base import BaseHTTPMiddleware
from src.config.database import SessionLocal
from src.models.entities import Audit
import logging
class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request,call_next):
        response=await call_next(request)
        if request.method in ('POST','PUT','PATCH','DELETE'):
            try:
                with SessionLocal() as db:
                    db.add(Audit(actor=getattr(request.state,'actor','anonymous'),action=f'{request.method} {request.url.path}',status=response.status_code,created_at=datetime.now(timezone.utc).isoformat()));db.commit()
            except Exception: logging.exception('audit write failed')
        return response
