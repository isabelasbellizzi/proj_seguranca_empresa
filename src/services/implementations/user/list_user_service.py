from dataclasses import dataclass
from typing import List

from src.infra.repositories.interfaces.iuser_repository import IUserRepository
from src.services.DTOs.user.user_response_service_dto import UserResponseServiceDto
from src.services.implementations.user.user_utilis import UserUtilis

@dataclass
class ListUserService:

    @staticmethod
    def execute(repo: IUserRepository, max_records=0) -> List[UserResponseServiceDto]:  # type: ignore
        user_list: List[UserResponseServiceDto] = []

        for element in repo.get_all(max_records=max_records):
            user_list.append(UserUtilis().user_2_user_dto(element))

        return user_list
