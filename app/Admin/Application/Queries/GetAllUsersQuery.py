from dataclasses import dataclass


@dataclass(frozen=True)
class GetAllUsersQuery:
    """Query para obtener todos los usuarios."""
    pass
