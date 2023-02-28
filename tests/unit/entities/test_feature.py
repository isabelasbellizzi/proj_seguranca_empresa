from src.domain.entities import Feature
from src.domain.enums.status_enum import StatusEnum
from src.domain.validators.big_int_validator import BigIntValidator
from src.domain.validators.enum_validator import EnumValidator


def test_feature_all_fields_ok(mocker):
    features = Feature(
        feature_id=1,
        paper_id=100,
        function_id=1000,
        status=StatusEnum.ACTIVE,
        create=True,
        read=True,
        update=True,
        delete=True
    )
    mocker.patch.object(EnumValidator, 'validate')
    mocker.patch.object(BigIntValidator, 'validate')

    calls = [
        mocker.call(features.feature_id, 'feature_id'),
        mocker.call(features.paper_id, 'paper_id'),
        mocker.call(features.function_id, 'function_id')
    ]

    features.validate()

    BigIntValidator.validate.assert_has_calls(calls)
    EnumValidator.validate.assert_called_once_with(features.status, "status", StatusEnum)
