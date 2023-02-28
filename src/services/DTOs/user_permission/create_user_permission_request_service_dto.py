from dataclasses import dataclass
from typing import List

@dataclass
class CreateUserPermissionRequestServiceDto():
    user_id: int
    paper_id: List[int]
