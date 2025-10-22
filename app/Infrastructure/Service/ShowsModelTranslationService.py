class ShowsModelTranslationService:
    
    @staticmethod
    def showsTranslation(
        show: dict,
    ):
        reducedMovieData = {
            "id": show['id'],
            "originalTitle": show['originalTitle'],
            "showType": show['showType'],
        }
        
        streamingOptions = {}
        for key in show['streamingOptions']:
            services = show['streamingOptions'][key]
            for service in services:
                streamingOptions = {
                    "service": service["service"]["name"],
                    "url": service["link"],
                }    
        reducedMovieData["streamingOptions"] = streamingOptions
        
        return reducedMovieData