"""
Tests unitarios para los validadores de Request del módulo Admin.
"""

import pytest
from Shared.Infrastructure.Validators.RequestValidator import (
    RequestValidator,
    ValidationError
)
from Admin.Infrastructure.Validators.RequestValidators import (
    CreateUserValidator,
    AddUserAddressValidator,
    UpdateUserAddressValidator,
)


class TestRequestValidator:
    """Tests para la clase base RequestValidator."""

    def test_empty_data_is_handled(self):
        """Debería manejar data None correctamente."""
        validator = RequestValidator(None)
        assert validator.data == {}

    def test_require_field_fails_when_missing(self):
        """Debería fallar cuando falta un campo requerido."""
        validator = RequestValidator({})
        result = validator._require_field("username")
        
        assert result is False
        assert len(validator.errors) == 1
        assert validator.errors[0].field == "username"
        assert validator.errors[0].code == "required"

    def test_require_field_fails_when_empty_string(self):
        """Debería fallar cuando el campo es string vacío."""
        validator = RequestValidator({"username": "   "})
        result = validator._require_field("username")
        
        assert result is False

    def test_require_field_passes_when_present(self):
        """Debería pasar cuando el campo existe."""
        validator = RequestValidator({"username": "john"})
        result = validator._require_field("username")
        
        assert result is True
        assert len(validator.errors) == 0

    def test_validate_string_length_min(self):
        """Debería validar longitud mínima."""
        validator = RequestValidator({"name": "ab"})
        result = validator._validate_string_length("name", min_length=3)
        
        assert result is False
        assert validator.errors[0].code == "min_length"

    def test_validate_string_length_max(self):
        """Debería validar longitud máxima."""
        validator = RequestValidator({"name": "abcdef"})
        result = validator._validate_string_length("name", max_length=5)
        
        assert result is False
        assert validator.errors[0].code == "max_length"

    def test_validate_email_format_valid(self):
        """Debería aceptar email válido."""
        validator = RequestValidator({"email": "test@example.com"})
        result = validator._validate_email_format("email")
        
        assert result is True
        assert len(validator.errors) == 0

    def test_validate_email_format_invalid_no_at(self):
        """Debería rechazar email sin @."""
        validator = RequestValidator({"email": "testexample.com"})
        result = validator._validate_email_format("email")
        
        assert result is False
        assert validator.errors[0].code == "invalid_email"

    def test_validate_email_format_invalid_no_domain(self):
        """Debería rechazar email sin dominio."""
        validator = RequestValidator({"email": "test@"})
        result = validator._validate_email_format("email")
        
        assert result is False

    def test_get_errors_returns_list_of_dicts(self):
        """get_errors debería retornar lista de diccionarios."""
        validator = RequestValidator({})
        validator._require_field("field1")
        validator._require_field("field2")
        
        errors = validator.get_errors()
        
        assert len(errors) == 2
        assert isinstance(errors[0], dict)
        assert "field" in errors[0]
        assert "message" in errors[0]
        assert "code" in errors[0]

    def test_get_error_messages_returns_dict(self):
        """get_error_messages debería retornar {field: message}."""
        validator = RequestValidator({})
        validator._require_field("username")
        
        messages = validator.get_error_messages()
        
        assert "username" in messages
        assert "required" in messages["username"].lower()


class TestCreateUserValidator:
    """Tests para CreateUserValidator."""

    def test_valid_data_passes(self):
        """Debería pasar con datos válidos."""
        data = {
            "username": "john_doe",
            "email": "john@example.com"
        }
        validator = CreateUserValidator(data)
        
        assert validator.is_valid() is True
        assert len(validator.errors) == 0

    def test_missing_username_fails(self):
        """Debería fallar sin username."""
        data = {
            "email": "john@example.com"
        }
        validator = CreateUserValidator(data)
        
        assert validator.is_valid() is False
        fields_with_errors = [e.field for e in validator.errors]
        assert "username" in fields_with_errors

    def test_missing_email_fails(self):
        """Debería fallar sin email."""
        data = {
            "username": "john_doe"
        }
        validator = CreateUserValidator(data)
        
        assert validator.is_valid() is False
        fields_with_errors = [e.field for e in validator.errors]
        assert "email" in fields_with_errors

    def test_empty_data_fails(self):
        """Debería fallar con data vacía."""
        validator = CreateUserValidator({})
        
        assert validator.is_valid() is False
        assert len(validator.errors) >= 2  # Al menos username y email

    def test_none_data_fails(self):
        """Debería fallar con data None."""
        validator = CreateUserValidator(None)
        
        assert validator.is_valid() is False

    def test_invalid_email_format_fails(self):
        """Debería fallar con formato de email inválido."""
        data = {
            "username": "john_doe",
            "email": "not-an-email"
        }
        validator = CreateUserValidator(data)
        
        assert validator.is_valid() is False
        error_codes = [e.code for e in validator.errors]
        assert "invalid_email" in error_codes

    def test_username_too_long_fails(self):
        """Debería fallar con username demasiado largo."""
        data = {
            "username": "a" * 256,
            "email": "john@example.com"
        }
        validator = CreateUserValidator(data)
        
        assert validator.is_valid() is False
        error_codes = [e.code for e in validator.errors]
        assert "max_length" in error_codes

    def test_email_too_long_fails(self):
        """Debería fallar con email demasiado largo."""
        data = {
            "username": "john_doe",
            "email": "a" * 256 + "@example.com"
        }
        validator = CreateUserValidator(data)
        
        assert validator.is_valid() is False

    def test_multiple_errors_collected(self):
        """Debería recolectar múltiples errores."""
        data = {
            "username": "",
            "email": "invalid"
        }
        validator = CreateUserValidator(data)
        
        assert validator.is_valid() is False
        assert len(validator.errors) >= 2

    def test_valid_email_with_subdomain(self):
        """Debería aceptar email con subdominio."""
        data = {
            "username": "john_doe",
            "email": "john@mail.example.com"
        }
        validator = CreateUserValidator(data)
        
        assert validator.is_valid() is True

    def test_valid_email_with_plus(self):
        """Debería aceptar email con +."""
        data = {
            "username": "john_doe",
            "email": "john+tag@example.com"
        }
        validator = CreateUserValidator(data)
        
        assert validator.is_valid() is True

    def test_is_valid_can_be_called_multiple_times(self):
        """is_valid debería poder llamarse múltiples veces."""
        data = {"username": "john", "email": "john@example.com"}
        validator = CreateUserValidator(data)
        
        result1 = validator.is_valid()
        result2 = validator.is_valid()
        
        assert result1 == result2
        assert len(validator.errors) == 0  # No se duplican errores


class TestAddUserAddressValidator:
    """Tests para AddUserAddressValidator."""

    def test_valid_data_passes(self):
        """Debería pasar con datos válidos."""
        data = {
            "street": "123 Main St",
            "city": "New York",
            "country": "USA"
        }
        validator = AddUserAddressValidator(data)
        
        assert validator.is_valid() is True
        assert len(validator.errors) == 0

    def test_missing_street_fails(self):
        """Debería fallar sin street."""
        data = {
            "city": "New York",
            "country": "USA"
        }
        validator = AddUserAddressValidator(data)
        
        assert validator.is_valid() is False
        fields_with_errors = [e.field for e in validator.errors]
        assert "street" in fields_with_errors

    def test_missing_city_fails(self):
        """Debería fallar sin city."""
        data = {
            "street": "123 Main St",
            "country": "USA"
        }
        validator = AddUserAddressValidator(data)
        
        assert validator.is_valid() is False
        fields_with_errors = [e.field for e in validator.errors]
        assert "city" in fields_with_errors

    def test_missing_country_fails(self):
        """Debería fallar sin country."""
        data = {
            "street": "123 Main St",
            "city": "New York"
        }
        validator = AddUserAddressValidator(data)
        
        assert validator.is_valid() is False
        fields_with_errors = [e.field for e in validator.errors]
        assert "country" in fields_with_errors

    def test_empty_data_fails(self):
        """Debería fallar con data vacía."""
        validator = AddUserAddressValidator({})
        
        assert validator.is_valid() is False
        assert len(validator.errors) >= 3  # street, city, country

    def test_street_too_long_fails(self):
        """Debería fallar con street demasiado larga."""
        data = {
            "street": "a" * 256,
            "city": "New York",
            "country": "USA"
        }
        validator = AddUserAddressValidator(data)
        
        assert validator.is_valid() is False
        error_codes = [e.code for e in validator.errors]
        assert "max_length" in error_codes


class TestUpdateUserAddressValidator:
    """Tests para UpdateUserAddressValidator."""

    def test_valid_data_with_all_fields(self):
        """Debería pasar con todos los campos."""
        data = {
            "street": "456 Updated St",
            "city": "Los Angeles",
            "country": "USA"
        }
        validator = UpdateUserAddressValidator(data)
        
        assert validator.is_valid() is True

    def test_valid_data_with_only_street(self):
        """Debería pasar con solo street."""
        data = {"street": "456 Updated St"}
        validator = UpdateUserAddressValidator(data)
        
        assert validator.is_valid() is True

    def test_valid_data_with_only_city(self):
        """Debería pasar con solo city."""
        data = {"city": "Los Angeles"}
        validator = UpdateUserAddressValidator(data)
        
        assert validator.is_valid() is True

    def test_valid_data_with_only_country(self):
        """Debería pasar con solo country."""
        data = {"country": "Canada"}
        validator = UpdateUserAddressValidator(data)
        
        assert validator.is_valid() is True

    def test_empty_data_fails(self):
        """Debería fallar sin ningún campo."""
        validator = UpdateUserAddressValidator({})
        
        assert validator.is_valid() is False
        fields_with_errors = [e.field for e in validator.errors]
        assert "request" in fields_with_errors

    def test_street_too_long_fails(self):
        """Debería fallar con street demasiado larga."""
        data = {"street": "a" * 256}
        validator = UpdateUserAddressValidator(data)
        
        assert validator.is_valid() is False
        error_codes = [e.code for e in validator.errors]
        assert "max_length" in error_codes

    def test_city_too_long_fails(self):
        """Debería fallar con city demasiado larga."""
        data = {"city": "a" * 101}
        validator = UpdateUserAddressValidator(data)
        
        assert validator.is_valid() is False
        error_codes = [e.code for e in validator.errors]
        assert "max_length" in error_codes

    def test_country_too_long_fails(self):
        """Debería fallar con country demasiado largo."""
        data = {"country": "a" * 101}
        validator = UpdateUserAddressValidator(data)
        
        assert validator.is_valid() is False
        error_codes = [e.code for e in validator.errors]
        assert "max_length" in error_codes