from dataclasses import dataclass
from uuid import UUID


@dataclass
class UpdateUserRequestServiceDto():
    azure_id: UUID
    user_email: str
