class Unauthorized(Exception):
    def __init__(self, msg: str = "Unauthorized"):
        self.message = {"error": msg}

        super().__init__(self.message)