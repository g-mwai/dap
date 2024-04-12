

class InsufficientFundsError(Exception):
    """Exception raised when the user has insufficient funds."""

    def __init__(self, message='You have insufficient funds to create this post'):
        self.message = message
        super().__init__(self.message)

