from src.infra.repositories.implementations import \
    OwnerRepository
from src.services.implementations.owner import \
    ListOwnerService, OwnerUtils
from src.services.DTOs.owner import \
    ListOwnerServiceRequestDTO
from src.domain.entities import Owner
from tests.unit.services.teste_service_base import TestServiceBase


class TestListFunction(TestServiceBase):
    def test_list_execute_parameters_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = OwnerRepository(db)
        max_records = 5
        system_id = 1234
        user_id = 4321

        data = ListOwnerServiceRequestDTO(max_records=max_records, system_id=system_id, user_id=user_id)
        owner = Owner(owner_id=123, system_id=321, user_id=321)

        mocker.patch.object(OwnerRepository, 'get_all', return_value = [owner])
        mocker.patch.object(OwnerUtils, 'owner_2_owner_dto')

        # Act
        ListOwnerService.execute(repo, data=data)

        # Assert
        OwnerRepository.get_all.assert_called_once_with(data=data)
        OwnerUtils.owner_2_owner_dto.assert_called_once_with(owner)
