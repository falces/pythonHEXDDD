import requests
from flask import current_app as app
from Shared.Domain.Exceptions.HTTPGetRequestException import HTTPGetRequestException

class APITools:
    def __init__(
        self,
        host: str,
        headers: dict = None
    ):
        self.host = host
        self.headers = headers

    def get(
        self,
        endpoint: str,
        params: dict = None,
    ) -> requests.Response:
        try:
            response = requests.get(
                url = self.host + endpoint,
                params = params,
                headers = self.headers,
            )
            
            self.__logAPIRequest(
                url = self.host + endpoint,
                method = 'GET',
                params = params,
                responseCount = len(response.content),
            )
            
            response.raise_for_status()

            return response
        
        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.RequestException,
                ) as e:
            raise HTTPGetRequestException(f"An error occurred: {e}", e.response.status_code)

    def post(
        self,
        url: str,
        data: dict = None,
        json: dict = None,
        headers: dict = None
    ) -> requests.Response:
        response = requests.post(
            self.host + url,
            data=data,
            json=json,
            headers=headers
        )
        return response
    
    def __logAPIRequest(
        self,
        url: str,
        method: str,
        params: dict = None,
        responseCount: int = None,
    ):
        queryString = ''
        for param in params:
            queryString += param + '=' + params[param] + '&'

        app.logger.info("Request: [" + method + "]" + url)
        app.logger.info("QueryString: " + queryString)
        app.logger.info("Lines: " + str(responseCount))