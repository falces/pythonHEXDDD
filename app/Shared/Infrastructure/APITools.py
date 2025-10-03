import requests
from flask import current_app as app
from Shared.Domain.Exceptions.HTTPGetRequestException import HTTPGetRequestException

class APITools:
    def __init__(self):
        pass

    def get(
        self,
        endpoint: str,
        params: dict = None,
        resultsInFile: bool = False,
        fileName: str = None,
    ) -> requests.Response:
        try:
            response = requests.get(
                url = app.config['HOST'] + endpoint,
                params = params,
                headers = {
                            'fulfilmentcrowd-api-key': app.config['API_KEY'],
                        },
            )
            response.raise_for_status()
            if response.status_code == 200:
                if resultsInFile:
                    self.createExcelFromAPIResponse(response.json(), fileName)
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
            app.config['HOST'] + url,
            data=data,
            json=json,
            headers=headers
        )
        return response

    def createExcelFromAPIResponse(
        self,
        data: dict,
        fileName: str
    ) -> None:
        import pandas as pd

        df = pd.DataFrame(data)
        df.to_excel('.' + '/output/' + fileName, index=False)