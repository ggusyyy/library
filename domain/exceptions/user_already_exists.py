class UserAlreadyExists(Exception):
    def __init__(self):
        super().__init__("This user already exists.")