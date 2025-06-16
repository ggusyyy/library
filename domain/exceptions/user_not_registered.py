class UserNotRegistered(Exception):
    def __init__(self):
        super().__init__("This user is not registered.")