class ControllerBase():

    @staticmethod
    def formatResponse(
        data: list,
        code: int,
    ) -> list:
        return {
            "status": "ok",
            "data": data,
        }, code
