class UserCantBorrowMore(Exception):
    def __init__(self):
        super().__init__("This user can't borrow more books.")