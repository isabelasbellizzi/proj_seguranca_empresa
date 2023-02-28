import pytest

from src.domain.entities import Owner
from src.infra.repositories.implementations import (OwnerRepository,
                                                    SystemRepository,
                                                    UserRepository)
from src.services.DTOs.owner import \
    CreateOwnerRequestServiceDto, ListOwnerServiceRequestDTO
from src.services.implementations.owner import OwnerUtils
from src.services.implementations.owner import \
    InsertOwnerService
from tests.unit.services.teste_service_base import DbHandlerFake, TestServiceBase


class TestInsertOwner(TestServiceBase):
    def test_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = OwnerRepository(db)
        system_repo = SystemRepository(db)
        user_repo = UserRepository(db)
        system_id = 1234
        user_id = 4321

        create_owner_dto = CreateOwnerRequestServiceDto(system_id=system_id, user_id=user_id)
        new_owner = Owner(**create_owner_dto.__dict__)
        list_owner_dto = ListOwnerServiceRequestDTO(system_id=new_owner.system_id, user_id=new_owner.user_id)

        mocker.patch.object(Owner, 'validate')
        mocker.patch.object(SystemRepository, 'get', return_value=True)
        mocker.patch.object(UserRepository, 'get_by_user_id', return_value=True)
        mocker.patch.object(OwnerRepository, 'get_all', return_value=[])
        mocker.patch.object(OwnerRepository, 'add')
        mocker.patch.object(DbHandlerFake, 'commit')
        mocker.patch.object(OwnerUtils, 'owner_2_owner_dto')

        # Act
        InsertOwnerService.execute(db=db, repo=repo, system_repo=system_repo, user_repo=user_repo, data=create_owner_dto)

        # Assert
        Owner.validate.assert_called_once_with()
        SystemRepository.get.assert_called_once_with(system_id=system_id)
        UserRepository.get_by_user_id.assert_called_once_with(user_id=user_id)
        OwnerRepository.get_all.assert_called_once_with(data=list_owner_dto)
        OwnerRepository.add.assert_called_once_with(new_owner)
        DbHandlerFake.commit.assert_called_once_with()
        OwnerUtils.owner_2_owner_dto.assert_called_once_with(new_owner)

    def test_execute_system_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = OwnerRepository(db)
        system_repo = SystemRepository(db)
        user_repo = UserRepository(db)
        system_id = 1234
        user_id = 4321

        create_owner_dto = CreateOwnerRequestServiceDto(system_id=system_id, user_id=user_id)

        mocker.patch.object(Owner, 'validate')
        mocker.patch.object(SystemRepository, 'get', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            InsertOwnerService.execute(db=db, repo=repo, system_repo=system_repo, user_repo=user_repo, data=create_owner_dto)

        # Assert
        assert str(error.value) == f"System not found. [system_id={system_id}]"

    def test_execute_user_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = OwnerRepository(db)
        system_repo = SystemRepository(db)
        user_repo = UserRepository(db)
        system_id = 1234
        user_id = 4321

        create_owner_dto = CreateOwnerRequestServiceDto(system_id=system_id, user_id=user_id)

        mocker.patch.object(Owner, 'validate')
        mocker.patch.object(SystemRepository, 'get', return_value=True)
        mocker.patch.object(UserRepository, 'get_by_user_id', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            InsertOwnerService.execute(db=db, repo=repo, system_repo=system_repo, user_repo=user_repo, data=create_owner_dto)

        # Assert
        assert str(error.value) == f"User not found. [user_id={user_id}]"

    def test_execute_duplicated_object_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = OwnerRepository(db)
        system_repo = SystemRepository(db)
        user_repo = UserRepository(db)
        system_id = 1234
        user_id = 4321

        create_owner_dto = CreateOwnerRequestServiceDto(system_id=system_id, user_id=user_id)
        owner = Owner(owner_id=123, system_id=321, user_id=321)

        mocker.patch.object(Owner, 'validate')
        mocker.patch.object(SystemRepository, 'get', return_value=True)
        mocker.patch.object(UserRepository, 'get_by_user_id', return_value=True)
        mocker.patch.object(OwnerRepository, 'get_all', return_value=[owner])

        # Act
        with pytest.raises(Exception) as error:
            InsertOwnerService.execute(db=db, repo=repo, system_repo=system_repo, user_repo=user_repo, data=create_owner_dto)

        # Assert
        assert str(error.value) == f"This owner already exists. [owner_id={owner.owner_id}]"
