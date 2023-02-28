from pydantic import BaseModel

from src.domain.enums import FunctionTypeEnum

class FunctionCreateRequest(BaseModel):
    name: str
    function_type: FunctionTypeEnum
    system_id: int
