import pytest

from src.infra.repositories.implementations import \
    OwnerRepository
from src.services.exceptions import ServiceLayerNotFoundError
from src.services.implementations.owner import DeleteOwnerService
from tests.unit.services.teste_service_base import TestServiceBase, DbHandlerFake

class TestDeleteOwner(TestServiceBase):
    def test_execute_not_found_error(self, mocker):
        # Arrange
        owner_id = 1234
        db = self.db_handler
        repo = OwnerRepository(db=db)

        mocker.patch.object(OwnerRepository, 'get', return_value=None)

        # Act
        with pytest.raises(ServiceLayerNotFoundError) as error:
            DeleteOwnerService.execute(db=db, repo=repo, owner_id=owner_id)

        # Assert
        assert str(error.value) == f"Owner not found. [owner_id={owner_id}]"

    def test_execute_ok(self, mocker):
        # Arrange
        owner_id = 1234
        db = self.db_handler
        repo = OwnerRepository(db=db)

        mocker.patch.object(OwnerRepository, 'get', return_value=True)
        mocker.patch.object(OwnerRepository, 'delete')
        mocker.patch.object(DbHandlerFake, 'commit')

        # Act
        DeleteOwnerService.execute(db=db, repo=repo, owner_id=owner_id)

        # Assert
        OwnerRepository.get.assert_called_once_with(id=owner_id)
        OwnerRepository.delete.assert_called_once_with(id=owner_id)
        DbHandlerFake.commit.assert_called_once_with()
