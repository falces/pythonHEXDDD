from typing import List, Optional, Dict
from flask import current_app as app
from Domain.Show.ShowRepositoryInterface import ShowRepositoryInterface
from Domain.Show.Show import Show
from Infrastructure.ExternalAPI.Models.ShowAPIModel import ShowAPIModel
from Infrastructure.ExternalAPI.Mappers.ShowMapper import ShowMapper
from Shared.Infrastructure.APITools import APITools


class ShowsAPIRepository(ShowRepositoryInterface):
    """
    Implementación del repositorio de Show que consulta la API externa Stream Availability.
    Esta clase pertenece a la capa de Infrastructure y traduce respuestas de API 
    a entidades de dominio puras.
    """
    
    def __init__(self, api_host: str = None, api_key: str = None):
        """
        Inicializa el repositorio con configuración de API.
        
        Args:
            api_host: Host de la API (opcional, usa config si no se proporciona)
            api_key: API key (opcional, usa config si no se proporciona)
        """
        host = api_host or app.config.get('STREAM_AVAILABILITY_HOST')
        key = api_key or app.config.get('STREAM_AVAILABILITY_KEY')
        
        if not host or not key:
            raise ValueError("API host and key must be configured")
        
        self.url = 'https://' + host + '/shows'
        headers = {
            'x-rapidapi-key': key,
            'x-rapidapi-host': host,
        }
        self.api_tools = APITools(self.url, headers)
    
    def find_by_criteria(self, criteria: Dict[str, any]) -> List[Show]:
        """
        Busca shows según criterios específicos consultando la API externa.
        
        Args:
            criteria: Diccionario con criterios de búsqueda
            
        Returns:
            Lista de entidades Show de dominio
        """
        try:
            response = self.api_tools.get(
                endpoint='/search/filters',
                params=criteria,
            ).json()
            
            shows = []
            for show_data in response.get("shows", []):
                # Convertir respuesta API a modelo de API
                api_model = ShowAPIModel.fromAPIResponse(show_data)
                
                # Convertir modelo de API a entidad de dominio
                domain_entity = ShowMapper.toDomain(api_model)
                
                if domain_entity is not None:
                    shows.append(domain_entity)
            
            return shows
            
        except Exception as e:
            app.logger.error(f"Error fetching shows from API: {e}")
            return []
    
    def find_by_id(self, show_id: str) -> Optional[Show]:
        """
        Busca un show por su ID en la API externa.
        
        Args:
            show_id: Identificador del show
            
        Returns:
            Show o None si no existe
        """
        try:
            response = self.api_tools.get(
                endpoint=f'/{show_id}',
                params={}
            ).json()
            
            if response:
                api_model = ShowAPIModel.fromAPIResponse(response)
                return ShowMapper.toDomain(api_model)
            
            return None
            
        except Exception as e:
            app.logger.error(f"Error fetching show {show_id} from API: {e}")
            return None