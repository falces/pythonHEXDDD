"""
Validadores de Request para el módulo Admin.
"""

from Shared.Infrastructure.Validators.RequestValidator import RequestValidator


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
