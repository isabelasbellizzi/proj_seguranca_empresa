import pytest

from src.domain.validators.email_validator import EmailValidator


class TestEmailValidator:
    def test_email_validator_none_error(self):
        # Arrange
        email = None

        # Act
        with pytest.raises(Exception) as error:
            EmailValidator.validate(email)   # type: ignore

        # Assert
        assert str(error.value) == "invalid E-mail. [value=]"

    def test_email_validator_invalid_error(self):
        # Arrange
        email = "teste@teste"

        # Act
        with pytest.raises(Exception) as error:
            EmailValidator.validate(email)   # type: ignore

        # Assert
        assert str(error.value) == f"invalid E-mail. [value={email}]"


    def test_email_validator_invalid_with_leading_whitespace_error(self):
        # Arrange
        email = " teste@teste"

        # Act
        with pytest.raises(Exception) as error:
            EmailValidator.validate(email)   # type: ignore

        # Assert
        assert str(error.value) == "invalid E-mail. [value=teste@teste]"

    def test_email_validator_invalid_with_trailing_whitespace_error(self):
        # Arrange
        email = "teste@teste "

        # Act
        with pytest.raises(Exception) as error:
            EmailValidator.validate(email)   # type: ignore

        # Assert
        assert str(error.value) == "invalid E-mail. [value=teste@teste]"

    def test_email_validator_invalid_with_trailing_and_leading_whitespaces_error(self):
        # Arrange
        email = " teste@teste "

        # Act
        with pytest.raises(Exception) as error:
            EmailValidator.validate(email)   # type: ignore

        # Assert
        assert str(error.value) == "invalid E-mail. [value=teste@teste]"

        # Assert
        assert str(error.value) == "invalid E-mail. [value=teste@teste]"

    def test_email_validator_invalid_empty_field_error(self):
        # Arrange
        email = ""

        # Act
        with pytest.raises(Exception) as error:
            EmailValidator.validate(email)   # type: ignore

        # Assert
        assert str(error.value) == f"invalid E-mail. [value={email}]"

    def test_email_validator_invalid_empty_field_with_whitespaces_error(self):
        # Arrange
        email = "         "

        # Act
        with pytest.raises(Exception) as error:
            EmailValidator.validate(email)   # type: ignore

        # Assert
        assert str(error.value) == "invalid E-mail. [value=]"
