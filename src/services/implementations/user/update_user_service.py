from dataclasses import dataclass
from src.infra.adaptors.db_adapter.idb_handler import IDbHandler
from src.infra.repositories.interfaces.iuser_repository import IUserRepository
from src.services.DTOs.user.update_user_request_service_dto import UpdateUserRequestServiceDto
from src.services.exceptions.service_layer_duplicated_name_error import \
    ServiceLayerDuplicatedNameError
from src.services.exceptions.service_layer_notfound_error import \
    ServiceLayerNotFoundError


@dataclass
class UpdateUserService:

    @staticmethod
    def execute(db: IDbHandler, repo: IUserRepository, user_id: int, data: UpdateUserRequestServiceDto) -> None:

        user_read = repo.get_by_email(user_email=data.user_email)
        ServiceLayerDuplicatedNameError.when(user_read is not None, f"There is already a user with that email. [user_email=[{data.user_email}]")

        user = repo.get_by_user_id(user_id=user_id)
        ServiceLayerNotFoundError.when(user is None, f"User not found. [user_id={user_id}]")

        user.azure_id = data.azure_id  # type: ignore
        user.user_email = data.user_email  # type: ignore

        repo.update(user)  # type: ignore
        db.commit()
