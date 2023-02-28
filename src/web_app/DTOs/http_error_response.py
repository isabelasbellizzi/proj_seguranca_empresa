from dataclasses import dataclass

@dataclass
class HttpErrorResponse:
    success: bool = False
    msg: str = ""
