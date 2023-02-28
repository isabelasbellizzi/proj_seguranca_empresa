from src.domain.entities.user_permission import UserPermission

from src.domain.enums.status_enum import StatusEnum
from src.domain.validators import BigIntValidator, EnumValidator


class TestUserPermission:

    def test_mock_validate_all_fields_ok(self, mocker):
        # Arrange
        user_permission = UserPermission(user_permission_id=1000, user_id=1234, paper_id=1, status=StatusEnum.ACTIVE)
        mocker.patch.object(BigIntValidator, 'validate')
        mocker.patch.object(EnumValidator, 'validate')

        calls = [
            mocker.call(user_permission.user_permission_id, 'user_permission_id'),
            mocker.call(user_permission.user_id, 'user_id'),
            mocker.call(user_permission.paper_id, 'paper_id')
        ]

        # Act
        user_permission.validate()

        # Assert
        BigIntValidator.validate.assert_has_calls(calls)
        EnumValidator.validate.assert_called_once_with(user_permission.status, "status", StatusEnum)
