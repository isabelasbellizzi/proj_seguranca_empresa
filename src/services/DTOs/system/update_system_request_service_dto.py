from dataclasses import dataclass
from uuid import UUID


@dataclass
class UpdateSystemRequestServiceDto():
    token_id: UUID
    system_name: str
