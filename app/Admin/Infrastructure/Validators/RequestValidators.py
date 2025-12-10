"""
Validadores de Request para el módulo Admin.
"""

from Shared.Infrastructure.Validators.RequestValidator import RequestValidator, ValidationError


class CreateUserValidator(RequestValidator):
    """Validador para la creación de usuarios."""
    
    def _validate(self) -> None:
        # Validar campos requeridos
        self._require_field("username")
        self._require_field("email")
        
        # Validar tipos
        self._validate_type("username", str, "string")
        self._validate_type("email", str, "string")
        
        # Validar longitudes
        self._validate_string_length("username", min_length=1, max_length=255)
        self._validate_string_length("email", min_length=1, max_length=255)
        
        # Validar formato de email
        self._validate_email_format("email")


class UpdateUserValidator(RequestValidator):
    """Validador para la actualización de usuarios."""
    
    def _validate(self) -> None:
        # Al menos un campo debe estar presente
        has_username = self._data.get("username") is not None
        has_email = self._data.get("email") is not None
        
        if not has_username and not has_email:
            self._add_error("request", "At least one field (username or email) must be provided")
            return
        
        # Validar username si está presente
        if has_username:
            self._validate_type("username", str, "string")
            self._validate_string_length("username", min_length=1, max_length=255)
        
        # Validar email si está presente
        if has_email:
            self._validate_type("email", str, "string")
            self._validate_string_length("email", min_length=1, max_length=255)
            self._validate_email_format("email")


class AddUserAddressValidator(RequestValidator):
    """Validador para añadir una dirección a un usuario."""
    
    def _validate(self) -> None:
        # Validar campos requeridos
        self._require_field("street")
        self._require_field("city")
        self._require_field("country")
        
        # Validar tipos
        self._validate_type("street", str, "string")
        self._validate_type("city", str, "string")
        self._validate_type("country", str, "string")
        
        # Validar longitudes
        self._validate_string_length("street", min_length=1, max_length=255)
        self._validate_string_length("city", min_length=1, max_length=100)
        self._validate_string_length("country", min_length=1, max_length=100)


class UpdateUserAddressValidator(RequestValidator):
    """Validador para actualizar una dirección de usuario."""
    
    def _validate(self) -> None:
        # Al menos un campo debe estar presente
        has_street = self.data.get("street") is not None
        has_city = self.data.get("city") is not None
        has_country = self.data.get("country") is not None
        
        if not has_street and not has_city and not has_country:
            self.errors.append(ValidationError(
                field="request",
                message="At least one field (street, city or country) must be provided",
                code="missing_fields"
            ))
            return
        
        # Validar street si está presente
        if has_street:
            self._validate_type("street", str, "string")
            self._validate_string_length("street", min_length=1, max_length=255)
        
        # Validar city si está presente
        if has_city:
            self._validate_type("city", str, "string")
            self._validate_string_length("city", min_length=1, max_length=100)
        
        # Validar country si está presente
        if has_country:
            self._validate_type("country", str, "string")
            self._validate_string_length("country", min_length=1, max_length=100)
