import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request,call_next):
        try: return await call_next(request)
        except IntegrityError: return JSONResponse({'detail':'编号或方案标题重复，请修改后重试'},status_code=409)
        except Exception:
            logging.exception('request failed')
            return JSONResponse({'detail':'服务暂时不可用，请重试'},status_code=500)
