"""
Validador base para Requests.
Proporciona validación escalable y reutilizable para los datos de entrada.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Representa un error de validación."""
    field: str
    message: str
    code: str = "invalid"


class RequestValidator:
    """
    Validador base para requests.
    Proporciona métodos comunes de validación.
    
    Para crear un validador específico, heredar de esta clase
    y sobrescribir el método _validate().
    
    Ejemplo:
        class CreateUserValidator(RequestValidator):
            def _validate(self) -> None:
                self._require_field("username")
                self._require_field("email")
                self._validate_email_format("email")
    """
    
    def __init__(self, data: Optional[Dict[str, Any]]):
        self.data = data or {}
        self.errors: List[ValidationError] = []
    
    def is_valid(self) -> bool:
        """Ejecuta las validaciones y retorna si es válido."""
        self.errors = []
        self._validate()
        return len(self.errors) == 0
    
    def _validate(self) -> None:
        """Método a sobrescribir en clases hijas."""
        pass
    
    def get_errors(self) -> List[Dict[str, str]]:
        """Retorna los errores en formato diccionario."""
        return [
            {
                "field": error.field,
                "message": error.message,
                "code": error.code
            }
            for error in self.errors
        ]
    
    def get_error_messages(self) -> Dict[str, str]:
        """Retorna los errores como {field: message}."""
        return {error.field: error.message for error in self.errors}
    
    # ========== Métodos de validación reutilizables ==========
    
    def _require_field(self, field: str, message: Optional[str] = None) -> bool:
        """Valida que un campo exista y no esté vacío."""
        value = self.data.get(field)
        if value is None or (isinstance(value, str) and value.strip() == ""):
            self.errors.append(ValidationError(
                field=field,
                message=message or f"Field '{field}' is required",
                code="required"
            ))
            return False
        return True
    
    def _validate_string_length(
        self,
        field: str,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> bool:
        """Valida la longitud de un string."""
        value = self.data.get(field)
        if not isinstance(value, str):
            return True  # Si no es string, otra validación lo capturará
        
        if min_length is not None and len(value) < min_length:
            self.errors.append(ValidationError(
                field=field,
                message=f"Field '{field}' must be at least {min_length} characters",
                code="min_length"
            ))
            return False
        
        if max_length is not None and len(value) > max_length:
            self.errors.append(ValidationError(
                field=field,
                message=f"Field '{field}' must be at most {max_length} characters",
                code="max_length"
            ))
            return False
        
        return True
    
    def _validate_email_format(self, field: str) -> bool:
        """Valida formato básico de email."""
        value = self.data.get(field)
        if not isinstance(value, str):
            return True
        
        # Validación básica: contiene @ y al menos un punto después
        if "@" not in value or "." not in value.split("@")[-1]:
            self.errors.append(ValidationError(
                field=field,
                message=f"Field '{field}' must be a valid email address",
                code="invalid_email"
            ))
            return False
        
        return True
    
    def _validate_type(self, field: str, expected_type: type, type_name: str) -> bool:
        """Valida el tipo de un campo."""
        value = self.data.get(field)
        if value is not None and not isinstance(value, expected_type):
            self.errors.append(ValidationError(
                field=field,
                message=f"Field '{field}' must be a {type_name}",
                code="invalid_type"
            ))
            return False
        return True
