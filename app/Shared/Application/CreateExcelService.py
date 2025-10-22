class CreateExcelService:
    
    @staticmethod
    def createExcelFromAPIResponse(
        data: dict,
        fileName: str
    ) -> None:
        import pandas as pd

        df = pd.DataFrame(data)
        df.to_excel('.' + '/output/' + fileName, index=False)