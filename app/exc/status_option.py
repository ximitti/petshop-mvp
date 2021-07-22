class InvalidKeysError(Exception):
    def __init__(self, data: dict, feild_options: list) -> None:
        self.message = (
            {
                "error": {
                    "valid_options": feild_options,
                    "recieved_option": list(data.keys()),
                }
            },
        )

        super().__init__(self.message)


class MissingKeysError(Exception):
    def __init__(self, required_fields: list, missing_keys: list) -> None:
        self.message = (
            {
                "error": {
                    "required_fields": required_fields,
                    "missing_keys": missing_keys,
                }
            },
        )

        super().__init__(self.message)
