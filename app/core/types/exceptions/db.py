class NotFoundModelError(Exception):
    def __init__(self, id: int, model: str):
        self.id = id
        self.model = model
