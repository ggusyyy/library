class BookNotFound(Exception):
    def __init__(self):
        super().__init__("Book not found.")