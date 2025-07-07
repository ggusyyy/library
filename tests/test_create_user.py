from uuid import uuid4

import pytest

from application.dtos.create_user import CreateUserDTO
from application.use_cases.create_user import CreateUserUseCase
from domain.exceptions.user_already_exists import UserAlreadyExists
from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from infrastructure.repositories.user.in_memory_user_repository import InMemoryUserRepository


def test_created_user_succesfully() -> None:
    repo: UserRepository = InMemoryUserRepository()
    create_user: CreateUserUseCase = CreateUserUseCase(repo)
    gus: User = create_user.run(CreateUserDTO(str(uuid4()), "gus"))
    
    assert isinstance(gus, User)
    assert gus.name == "gus"
    assert gus.id is not None
    
def test_user_cant_register_if_already_exists() -> None:
    repo: UserRepository = InMemoryUserRepository()
    create_user: CreateUserUseCase = CreateUserUseCase(repo)
    gus: User = create_user.run(CreateUserDTO(str(uuid4()), "gus"))
    
    with pytest.raises(UserAlreadyExists):
        create_user.run(CreateUserDTO(gus.id, "gus"))
        