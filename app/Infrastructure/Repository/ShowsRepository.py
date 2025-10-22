from Shared.Domain.Repositories.AbstractRepository import AbstractRepository
from Shared.Infrastructure.APITools import APITools
from flask import current_app as app
from Infrastructure.Service.ShowsModelTranslationService import ShowsModelTranslationService


class ShowsRepository(AbstractRepository):    
    def __init__(self):
        host = app.config['STREAM_AVAILABILITY_HOST']
        self.url = 'https://' + host + '/shows'
        headers = {
                'x-rapidapi-key': app.config['STREAM_AVAILABILITY_KEY'],
                'x-rapidapi-host': host,
            }
        self.api_tools = APITools(self.url, headers)
    
    def findByCriteria(
        self,
        args: dict = None,
    ) -> dict:       
        response = self.api_tools.get(
            endpoint = '/search/filters',
            params = args,
        ).json()
        
        shows = []
        for show in response["shows"]:
            shows.append(ShowsModelTranslationService.showsTranslation(show))
        
        return shows
        
    def save(self):
        pass

    def findAll(self):
        pass

    def findById(self):
        pass