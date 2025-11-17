from typing import Optional


class StreamingOption:
    """
    Value Object para las opciones de streaming de un Show.
    """
    
    def __init__(
        self,
        service_name: str,
        url: Optional[str] = None
    ):
        if not service_name or len(service_name) == 0:
            raise ValueError("Service name cannot be empty")
        
        self._service_name = service_name
        self._url = url

    @staticmethod
    def create(service_name: str, url: Optional[str] = None) -> 'StreamingOption':
        return StreamingOption(service_name=service_name, url=url)
    
    def getServiceName(self) -> str:
        return self._service_name
    
    def getUrl(self) -> Optional[str]:
        return self._url
    
    def hasUrl(self) -> bool:
        return self._url is not None and len(self._url) > 0
    
    def toDict(self) -> dict:
        return {
            "service": self._service_name,
            "url": self._url
        }
