from application.dtos.create_user import CreateUserDTO
from domain.exceptions.user_already_exists import UserAlreadyExists
from domain.models.user import User

from domain.repositories.user_repository import UserRepository


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository,) -> None:
        self.user_repository: UserRepository = user_repository
    
    def run(self, input: CreateUserDTO) -> User:
        if self.user_repository.get_by_id(input.id):
            raise UserAlreadyExists()
        
        user: User = User(input.id, input.name)
        self.user_repository.save(user)
        return user