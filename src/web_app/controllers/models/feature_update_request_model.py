from typing import Optional
from pydantic import BaseModel

class FeatureUpdateRequest(BaseModel):
    create: Optional[bool] = None
    read: Optional[bool] = None
    update: Optional[bool] = None
    delete: Optional[bool] = None
