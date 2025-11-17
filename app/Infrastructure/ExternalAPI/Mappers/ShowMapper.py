from Domain.Show.Show import Show
from Domain.Show.ValueObjects.ShowId import ShowId
from Domain.Show.ValueObjects.ShowTitle import ShowTitle
from Domain.Show.ValueObjects.ShowType import ShowType
from Domain.Show.ValueObjects.StreamingOption import StreamingOption
from Infrastructure.ExternalAPI.Models.ShowAPIModel import ShowAPIModel
from typing import Optional


class ShowMapper:
    """
    Mapper para convertir entre la entidad de dominio Show 
    y el modelo de API externa ShowAPIModel.
    """

    @staticmethod
    def toDomain(api_model: ShowAPIModel) -> Optional[Show]:
        """
        Convierte un modelo de API externa a una entidad de dominio.
        
        Args:
            api_model: ShowAPIModel de la API externa
            
        Returns:
            Show: Entidad de dominio o None si hay error
        """
        if api_model is None:
            return None
        
        try:
            show_id = ShowId.create(api_model.show_id)
            title = ShowTitle.create(api_model.original_title)
            show_type = ShowType.create(api_model.show_type)
            
            streaming_option = None
            if api_model.streaming_options and 'service' in api_model.streaming_options:
                streaming_option = StreamingOption.create(
                    service_name=api_model.streaming_options['service'],
                    url=api_model.streaming_options.get('url')
                )
            
            return Show(
                show_id=show_id,
                title=title,
                show_type=show_type,
                streaming_option=streaming_option
            )
        except Exception as e:
            # Log error y retornar None si la conversión falla
            print(f"Error mapping API model to domain: {e}")
            return None

    @staticmethod
    def toDict(entity: Show) -> dict:
        """
        Convierte una entidad de dominio a diccionario para serialización.
        
        Args:
            entity: Entidad de dominio Show
            
        Returns:
            dict: Representación en diccionario
        """
        result = {
            "id": entity.getId(),
            "originalTitle": entity.getTitle(),
            "showType": entity.getType(),
        }
        
        if entity.hasStreamingOption():
            result["streamingOptions"] = entity.getStreamingOption().toDict()
        else:
            result["streamingOptions"] = {}
        
        return result

    @staticmethod
    def toDictList(entities: list[Show]) -> list[dict]:
        """
        Convierte una lista de entidades a lista de diccionarios.
        
        Args:
            entities: Lista de entidades Show
            
        Returns:
            list[dict]: Lista de diccionarios
        """
        return [ShowMapper.toDict(entity) for entity in entities if entity is not None]
