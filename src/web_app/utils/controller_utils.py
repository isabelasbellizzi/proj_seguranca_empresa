from dataclasses import dataclass
from fastapi import Response, status
from src.web_app.DTOs.http_error_response import HttpErrorResponse

@dataclass
class ControllweUtils:
    @staticmethod
    def response_http_error_response(msg: str, status_code: status) -> Response:
        return Response(HttpErrorResponse(success=False, message=msg), status_code=status_code)
