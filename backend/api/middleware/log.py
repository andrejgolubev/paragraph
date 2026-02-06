import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from backend.core.config import settings
from ..logger import log


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # ID для трейсинга
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        start_time = time.perf_counter()
        
        log_dict = {
            'url': str(request.url),
            'method': request.method,
            'ip': (
                request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
                or request.headers.get("X-Real-IP")
                or (request.client.host if request.client else None)
            ),
            'user_agent': request.headers.get('user-agent'),
        }
        
        log.info("Request %s sent: %s", request_id, str(log_dict))
        
        try:
            response = await call_next(request)
            
            # после вызова эндпоинта:
            process_time = time.perf_counter() - start_time
            
            log_dict |= {
                'status_code': response.status_code,
                'process_time_ms': round(process_time * 1000, 2),
                'response_size': response.headers.get('content-length'),
            }
            
            status = response.status_code

            
            if 100 <= status < 200: 
                log.info("Request %s completed (informational): %s", request_id, status)
            if 200 <= status < 300: 
                log.info("Request %s completed with a success: %s", request_id, status)
            if 300 <= status < 400: 
                log.info("Request %s completed with a redirect: %s", request_id, status)
            elif 400 <= status < 500:
                log.info("Request %s completed with a client error: %s", request_id, status)
            else: 
                log.error("Request %s completed with a server error: %s", request_id, status)

            response.headers['X-Request-ID'] = request_id
            
            return response
            
        except Exception as exc:
            process_time = time.perf_counter() - start_time
            log_dict |= {
                'process_time_ms': round(process_time * 1000, 2),
                'error': str(exc),
                'error_type': type(exc).__name__,
            }
            log.error("Request %s failed", request_id, exc_info=True)
            raise
