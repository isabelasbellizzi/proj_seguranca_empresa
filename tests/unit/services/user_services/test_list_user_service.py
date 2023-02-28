from src.infra.repositories.implementations.user_repository import \
    UserRepository
from src.services.implementations.user.list_user_service import ListUserService
from tests.unit.services.teste_service_base import TestServiceBase


class TestListUser(TestServiceBase):

    def test_list_execute_ok(self, mocker):
        # Arrange
        db = self.db_handler
        repo = UserRepository(db=db)
        mocker.patch.object(UserRepository, 'get_all')

        # Act
        ListUserService.execute(repo=repo)

        # Assert
        UserRepository.get_all.assert_called_once_with(max_records=0)
