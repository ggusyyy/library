class UserDoesNotHaveTheBook(Exception):
    def __init__(self):
        super().__init__("This user does not have the book.")