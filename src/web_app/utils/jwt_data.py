from dataclasses import dataclass
@dataclass
class JWTData:
    user_id: int
    email: str
