class PasswordValidationError(ValueError):
    def __init__(self, message, requirements):
        super().__init__(message)
        self.message = message
        self.requirements = requirements
