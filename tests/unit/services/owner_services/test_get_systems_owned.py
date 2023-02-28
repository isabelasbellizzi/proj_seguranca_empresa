import pytest

from src.domain.entities import User, Owner
from src.infra.repositories.implementations import \
    OwnerRepository, SystemRepository, UserRepository
from src.services.DTOs.owner import ListOwnerServiceRequestDTO
from src.services.implementations.owner import GetSystemsOwnedService
from tests.unit.services.teste_service_base import TestServiceBase


class TestGetSystemsOwned(TestServiceBase):
    def test_execute_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = OwnerRepository(db)
        system_repo = SystemRepository(db)
        user_repo = UserRepository(db)
        user_email = "user@transfero.com"

        mocker.patch.object(UserRepository, 'get_by_email', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            GetSystemsOwnedService.execute(repo, system_repo=system_repo, user_repo=user_repo, user_email=user_email)

        # Assert
        assert str(error.value) == f"User not found. [user_email={user_email}"

    def test_execute_not_owner_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = OwnerRepository(db)
        system_repo = SystemRepository(db)
        user_repo = UserRepository(db)
        user_email = "user@transfero.com"
        user_id = 1

        user = User(user_id=user_id, user_email=user_email)

        mocker.patch.object(UserRepository, 'get_by_email', return_value=user)
        mocker.patch.object(OwnerRepository, 'get_all', return_value=[])

        # Act
        with pytest.raises(Exception) as error:
            GetSystemsOwnedService.execute(repo, system_repo=system_repo, user_repo=user_repo, user_email=user_email)

        # Assert
        assert str(error.value) == f"This user does not own a system. [user_id={user.user_id}]"

    def test_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = OwnerRepository(db)
        system_repo = SystemRepository(db)
        user_repo = UserRepository(db)
        user_email = "user@transfero.com"
        user_id = 1
        owner_id = 1
        system_id = 1

        user = User(user_id=user_id, user_email=user_email)
        owner = Owner(owner_id=owner_id, system_id=system_id, user_id=user_id)

        ListOwnerServiceRequestDTO(user_id=user_id)

        mocker.patch.object(UserRepository, 'get_by_email', return_value=user)
        mocker.patch.object(OwnerRepository, 'get_all', return_value=[owner])
        mocker.patch.object(SystemRepository, 'get')

        # Act
        GetSystemsOwnedService.execute(repo, system_repo=system_repo, user_repo=user_repo, user_email=user_email)

        # Assert
        UserRepository.get_by_email.assert_called_once_with(user_email=user_email)
        OwnerRepository.get_all.assert_called_once_with(data=ListOwnerServiceRequestDTO(user_id=user_id))
        SystemRepository.get.assert_called_once_with(system_id=system_id)
