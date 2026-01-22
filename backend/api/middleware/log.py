import json
import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
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
            'ip': request.client.host if request.client else None,
            'user_agent': request.headers.get('user-agent'),
        }
        
        log.info("Request %s sent: %s", request_id, json.dumps(log_dict), extra=log_dict)
        
        try:
            response = await call_next(request)
            
            # после вызова эндпоинта:
            process_time = time.perf_counter() - start_time
            
            log_dict |= {
                'status_code': response.status_code,
                'process_time_ms': round(process_time * 1000, 2),
                'response_size': response.headers.get('content-length'),
            }
            
            if response.status_code >= 400:
                log.warning("Request %s completed: %s", request_id, json.dumps(log_dict), extra=log_dict)
            else: 
                log.info("Request %s completed: %s", request_id, json.dumps(log_dict), extra=log_dict)

            response.headers['X-Request-ID'] = request_id
            
            return response
            
        except Exception as exc:
            process_time = time.perf_counter() - start_time
            log_dict |= {
                'process_time_ms': round(process_time * 1000, 2),
                'error': str(exc),
                'error_type': type(exc).__name__,
            }
            log.error("Request %s failed", request_id, extra=log_dict, exc_info=True)
            raise
