class BookNotAvailable(Exception):
    def __init__(self):
        super().__init__("Book not available.")