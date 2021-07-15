from http import HTTPStatus


class InvalidKeysError(Exception):
    def __init__(self, data: dict, feild_options: list) -> None:
        self.message = (
            {
                "error": {
                    "valid_options": feild_options,
                    "recieved_option": list(data.keys()),
                }
            },
            HTTPStatus.BAD_REQUEST,
        )

        super().__init__(self.message)
