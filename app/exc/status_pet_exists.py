class PetExistsError(Exception):
    def __init__(self, msg: str) -> None:
        self.message = {"error": msg}

        super().__init__(self.message)
