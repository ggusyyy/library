from uuid import uuid4
from dataclasses import dataclass
import pytest

from application.dtos.create_user import CreateUserDTO
from application.use_cases.create_user import CreateUserUseCase
from domain.exceptions.user_already_exists import UserAlreadyExists
from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from infrastructure.repositories.user.in_memory_user_repository import InMemoryUserRepository


@dataclass
class CreateUserSetup:
    repo: UserRepository
    use_case: CreateUserUseCase

@pytest.fixture
def create_user_setup() -> CreateUserSetup:
    repo: UserRepository = InMemoryUserRepository()
    use_case: CreateUserUseCase = CreateUserUseCase(repo)
    return CreateUserSetup(repo, use_case)


def test_created_user_succesfully(create_user_setup: CreateUserSetup) -> None:
    gus: User = create_user_setup.use_case.run(CreateUserDTO(str(uuid4()), "gus"))
    
    assert isinstance(gus, User)
    assert gus.name == "gus"
    assert gus.id is not None
    
def test_user_cant_register_if_already_exists(create_user_setup: CreateUserSetup) -> None:
    gus: User = create_user_setup.use_case.run(CreateUserDTO(str(uuid4()), "gus"))
    
    with pytest.raises(UserAlreadyExists):
        create_user_setup.use_case.run(CreateUserDTO(gus.id, "gus"))
        