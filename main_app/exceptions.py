class ItemUnavailableError(Exception):
    """Exception raised for errors in the input item's qunatity.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Item unavailable"):
        self.message = message
        super().__init__(self.message)
