import pytest

from src.infra.repositories.implementations import \
    OwnerRepository
from src.services.implementations.owner.owner_utils import OwnerUtils
from src.services.implementations.owner import GetOwnerService
from src.domain.entities import Owner
from tests.unit.services.teste_service_base import TestServiceBase


class TestGetOwner(TestServiceBase):
    def test_execute_not_found_error(self, mocker):
        # Arrange
        db = self.db_handler
        repo = OwnerRepository(db)
        owner_id = 1234

        mocker.patch.object(OwnerRepository, 'get', return_value=None)

        # Act
        with pytest.raises(Exception) as error:
            GetOwnerService.execute(repo, owner_id=owner_id)

        # Assert
        assert str(error.value) == f"Owner not found. [owner_id={owner_id}]"

    def test_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = OwnerRepository(db)
        owner_id = 1234

        owner = Owner(owner_id=1234, system_id=1, user_id=1)

        mocker.patch.object(OwnerRepository, 'get', return_value=owner)
        mocker.patch.object(OwnerUtils, 'owner_2_owner_dto')

        # Act
        GetOwnerService.execute(repo, owner_id=owner_id)

        # Assert
        OwnerRepository.get.assert_called_once_with(id=owner_id)
        OwnerUtils.owner_2_owner_dto.assassert_called_once_with(owner)
