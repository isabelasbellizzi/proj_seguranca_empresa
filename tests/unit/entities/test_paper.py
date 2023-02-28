from typing import Any
from uuid import uuid4
import pytest
from src.domain.entities.paper import Paper
from src.domain.config.config_atributes import NAME_MAX_LEN
from src.domain.enums.status_enum import StatusEnum
from src.domain.validators import BigIntValidator, EnumValidator, MandatoryStringValidator


class TestPaper:

    @pytest.mark.parametrize(
        ('name'), (
            ("Paper name  "),
            (" Paper name"),
            (" Paper name  "),
            ("Paper name")
        )
    )
    def test_validate_name_strip_ok(self, name: str):
        paper = Paper(name=name, paper_id=1234, system_id=1234)

        # Act
        paper.validate()

        # Assert
        assert paper.name == "Paper name"

    def test_mock_validate_all_fields_ok(self, mocker):
        #arrange
        paper = Paper(name="Paper Name", system_id=1234, status=StatusEnum.ACTIVE)
        mocker.patch.object(MandatoryStringValidator, 'validate')
        mocker.patch.object(BigIntValidator, 'validate')
        mocker.patch.object(EnumValidator, 'validate')

        calls_bigint_validator = [
            mocker.call(paper.paper_id, "paper_id"),
            mocker.call(paper.system_id, "system_id")
        ]

        #act
        paper.validate()

        #assert
        MandatoryStringValidator.validate.assert_called_once_with(paper.name, "name", min_length=5, max_length=NAME_MAX_LEN)
        BigIntValidator.validate.assert_has_calls(calls_bigint_validator)
        EnumValidator.validate.assert_called_once_with(paper.status, "status", StatusEnum)

    def test_paper_validate_name_ok(self):
        #arrange

        paper = Paper(name="testetesteteste", system_id=1234, paper_id=1234)

        # Act
        paper.validate()

        # Assert
        assert True

    min_size_name = 5
    default_msg_name_min_size = f"name minimum size is - {min_size_name}"

    @pytest.mark.parametrize(

        ('name', 'msg_erro'), (
            (None, "name isn't a string"),
            ("      ", "name must not be empty"),
            ('1234', default_msg_name_min_size),
            ("1" * (NAME_MAX_LEN + 1), f"name maximum size is - {NAME_MAX_LEN}"),
            ("  sejo    ", default_msg_name_min_size),
            ("", "name must not be empty")))
    def test_validate_name_error(self, name: Any, msg_erro: str):
        paper = Paper(name=name)

        # Act
        with pytest.raises(Exception) as erro:
            paper.validate()

        # Assert
        assert str(erro.value) == msg_erro

    def test_validate_created_without_parameters_error(self):
        # Arrange
        paper = Paper()

        # Act
        with pytest.raises(Exception) as erro:
            paper.validate()

        # Assert
        assert str(erro.value) == "name must not be empty"

    def test_paper_validate_system_id_and_paper_id_ok(self):
        #arrange

        paper = Paper(name="testetesteteste", system_id=1234, paper_id=1234)

        # Act
        paper.validate()

        # Assert
        assert True

    def test_paper_validate_system_id_none(self):
        value = None
        paper = Paper(name="testetesteteste", system_id=value, paper_id=12)  # type: ignore

        # Act
        with pytest.raises(Exception) as erro:
            paper.validate()

        # Assert
        assert str(erro.value) == f"Field system_id must be an BigInt. [value={value}]"

    def test_paper_validate_paper_id_not_int_error(self):
        value = "12"
        paper = Paper(name="testetesteteste", system_id=uuid4(), paper_id=value)  # type: ignore

        # Act
        with pytest.raises(Exception) as erro:
            paper.validate()

        # Assert
        assert str(erro.value) == f"Field paper_id must be an BigInt. [value={value}]"

    def test_paper_validate_paper_id_none(self):
        value = None
        paper = Paper(name="testetesteteste", system_id=uuid4(), paper_id=value)   # type: ignore

        # Act
        with pytest.raises(Exception) as erro:
            paper.validate()

        # Assert
        assert str(erro.value) == f"Field paper_id must be an BigInt. [value={value}]"


    def test_paper_validate_status_ok(self):
        value = 2
        paper = Paper(name="testetesteteste", system_id=1234, paper_id=122, status=value)  # type: ignore

        # Act
        paper.validate()

        # Assert
        assert True

    def test_paper_validate_status_not_enum_error(self):
        field_name = "status"
        value = 5
        enum_class = StatusEnum
        paper = Paper(name="testetesteteste", system_id=1234, paper_id=12, status=value)  # type: ignore

        # Act
        with pytest.raises(Exception) as erro:
            paper.validate()

        # Assert
        assert str(erro.value) == f"Field {field_name} must be in {enum_class}. [value={value}]"
