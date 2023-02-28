from dataclasses import dataclass
from typing import Optional
from src.domain.entities import User
from src.services.implementations.user.user_utilis import UserUtilis
from src.infra.repositories.interfaces.iuser_repository import IUserRepository
from src.services.DTOs.user.user_response_service_dto import UserResponseServiceDto
from src.services.exceptions import ServiceLayerNotFoundError


@dataclass
class GetUserByIdService:

    @staticmethod
    def execute(repo: IUserRepository, user_id: int) -> UserResponseServiceDto:
        user: Optional[User] = repo.get_by_user_id(user_id=user_id)
        ServiceLayerNotFoundError.when(user is None, f"User not found. [user_id={user_id}]")

        return UserUtilis().user_2_user_dto(user)
