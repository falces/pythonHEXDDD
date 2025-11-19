from Domain.Show.ValueObjects.ShowId import ShowId
from Domain.Show.ValueObjects.ShowTitle import ShowTitle
from Domain.Show.ValueObjects.ShowType import ShowType
from Domain.Show.ValueObjects.StreamingOption import StreamingOption
from Shared.Domain.Entities.EntityBase import AggregateRootBase
from typing import Optional


class Show(AggregateRootBase):
    """
    Entidad de dominio Show - Aggregate Root.
    Representa un show (película o serie) con sus opciones de streaming.
    Esta entidad es pura y no conoce detalles de APIs externas o persistencia.
    """
    
    def __init__(
        self,
        show_id: ShowId,
        title: ShowTitle,
        show_type: ShowType,
        streaming_option: Optional[StreamingOption] = None
    ):
        self.show_id = show_id
        self.title = title
        self.show_type = show_type
        self.streaming_option = streaming_option
    
    def get_id(self) -> str:
        return self.show_id.value
    
    def get_title(self) -> str:
        return self.title.value
    
    def get_type(self) -> str:
        return self.show_type.value
    
    def get_streaming_option(self) -> Optional[StreamingOption]:
        return self.streaming_option
    
    def is_movie(self) -> bool:
        return self.show_type.is_movie()
    
    def is_series(self) -> bool:
        return self.show_type.is_series()
    
    def has_streaming_option(self) -> bool:
        return self.streaming_option is not None
