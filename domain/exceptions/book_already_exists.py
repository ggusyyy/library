class BookAlreadyExists(Exception):
    def __init__(self):
        super().__init__("This book already exists.")