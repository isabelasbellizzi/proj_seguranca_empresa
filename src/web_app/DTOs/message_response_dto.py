from pydantic import BaseModel

class MessageResponseDTO(BaseModel):
    msg: str
