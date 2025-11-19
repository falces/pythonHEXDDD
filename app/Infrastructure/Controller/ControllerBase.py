class ControllerBase():

    @staticmethod
    def format_response(
        data: list,
        code: int,
    ) -> list:
        return {
            "status": "ok",
            "data": data,
        }, code