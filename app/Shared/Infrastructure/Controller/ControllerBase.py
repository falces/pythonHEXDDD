class ControllerBase():

    @staticmethod
    def format_response(
        data: list,
        code: int,
    ) -> list:
        return {
            "data": data,
        }, code