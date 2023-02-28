from dataclasses import dataclass
from uuid import UUID

from src.domain.entities import User
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces.iuser_repository import IUserRepository
from src.services.DTOs.user.create_user_request_service_dto import \
    CreateUserRequestServiceDto
from src.services.DTOs.user.user_response_service_dto import \
    UserResponseServiceDto
from src.services.implementations.user.user_utilis import UserUtilis
from src.services.exceptions import ServiceLayerDuplicatedNameError


@dataclass
class InsertUserService:

    @staticmethod
    def create_user(user_email: str, azure_id: UUID) -> User:
        return User(azure_id=azure_id, user_email=user_email)

    @staticmethod
    def execute(repo: IUserRepository, db: IDbHandler, data: CreateUserRequestServiceDto) -> UserResponseServiceDto:

        user_read = repo.get_by_email(user_email=data.user_email)

        ServiceLayerDuplicatedNameError.when(user_read is not None, f"This email was already registered. [user_email={data.user_email}]")

        new_user = InsertUserService.create_user(user_email=data.user_email, azure_id=data.azure_id)
        repo.add(new_user)
        db.commit()

        return UserUtilis().user_2_user_dto(new_user)
