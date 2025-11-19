class CreateExcelService:
    
    @staticmethod
    def create_excel_from_api_response(
        data: dict,
        file_name: str
    ) -> None:
        import pandas as pd

        df = pd.DataFrame(data)
        df.to_excel('.' + '/output/' + file_name, index=False)