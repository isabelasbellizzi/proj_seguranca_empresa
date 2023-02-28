from src.domain.enums import StatusEnum
from src.domain.validators import (BigIntValidator, EnumValidator)
from src.domain.entities.owner import Owner
import pytest

class TestOwner:
    
    def test_all_fields_ok(self, mocker):
        # Arrange
        owner = Owner(owner_id=123, system_id=123, user_id=123, status=StatusEnum.ACTIVE)
        
        mocker.patch.object(EnumValidator, 'validate')
        mocker.patch.object(BigIntValidator, 'validate')
        
        calls = [
            mocker.call(owner.owner_id, 'owner_id'),
            mocker.call(owner.system_id, 'system_id'),
            mocker.call(owner.user_id,'user_id')
            ]

        # Act
        owner.validate()

        # Assert
        EnumValidator.validate.assert_called_once_with(owner.status, "status", StatusEnum)
        BigIntValidator.validate.assert_has_calls(calls)
    