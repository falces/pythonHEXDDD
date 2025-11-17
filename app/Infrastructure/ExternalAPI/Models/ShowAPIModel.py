from typing import Optional, Dict, Any


class ShowAPIModel:
    """
    Modelo de datos que representa la respuesta de la API externa (Stream Availability).
    Este modelo pertenece a la capa de Infrastructure y no debe usarse fuera de ella.
    """
    
    def __init__(
        self,
        show_id: str,
        original_title: str,
        show_type: str,
        streaming_options: Optional[Dict[str, Any]] = None
    ):
        self.show_id = show_id
        self.original_title = original_title
        self.show_type = show_type
        self.streaming_options = streaming_options or {}
    
    @staticmethod
    def fromAPIResponse(api_data: dict) -> 'ShowAPIModel':
        """
        Crea un ShowAPIModel desde la respuesta de la API.
        
        Args:
            api_data: Diccionario con los datos de la API externa
            
        Returns:
            ShowAPIModel con los datos mapeados
        """
        # Extraer primera opción de streaming disponible
        streaming_options = {}
        if 'streamingOptions' in api_data and api_data['streamingOptions']:
            for country, services in api_data['streamingOptions'].items():
                if services and len(services) > 0:
                    first_service = services[0]
                    streaming_options = {
                        "service": first_service.get("service", {}).get("name", "Unknown"),
                        "url": first_service.get("link", "")
                    }
                    break  # Tomar solo la primera disponible
        
        return ShowAPIModel(
            show_id=api_data.get('id', ''),
            original_title=api_data.get('originalTitle', ''),
            show_type=api_data.get('showType', ''),
            streaming_options=streaming_options
        )
