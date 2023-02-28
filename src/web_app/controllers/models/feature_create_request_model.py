from typing import Optional
from pydantic import BaseModel

class FeatureCreateRequest(BaseModel):
    create: Optional[bool] = False
    read: Optional[bool] = False
    update: Optional[bool] = False
    delete: Optional[bool] = False
    paper_id: int
    function_id: int
