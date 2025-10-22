import requests
import json
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
            app.logger.info("Results: " + str(len(response.content)))
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