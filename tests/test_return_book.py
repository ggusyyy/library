from uuid import uuid4
from typing import Optional
from dataclasses import dataclass
import pytest

from application.use_cases.borrow_book import BorrowBookUseCase
from domain.exceptions.book_not_found import BookNotFound
from domain.exceptions.user_does_not_have_the_book import UserDoesNotHaveTheBook
from domain.models.book import Book
from domain.models.reputation import Reputation
from domain.models.user import User
from domain.repositories.book_repository import BookRepository
from domain.repositories.user_repository import UserRepository

from application.dtos.create_book import CreateBookDTO
from application.dtos.create_user import CreateUserDTO
from application.use_cases.create_book import CreateBookUseCase
from application.use_cases.create_user import CreateUserUseCase
from application.use_cases.return_book import ReturnBookUseCase

from infrastructure.repositories.book.in_memory_book_repository import InMemoryBookRepository
from infrastructure.repositories.user.in_memory_user_repository import InMemoryUserRepository

@dataclass
class ReturnBookSetup:
    user_repo: UserRepository
    book_repo: BookRepository
    create_user_use_case: CreateUserUseCase
    create_book_use_case: CreateBookUseCase
    return_book_use_case: ReturnBookUseCase
    borrow_book_use_case: BorrowBookUseCase

@pytest.fixture
def return_book_setup() -> ReturnBookSetup:
    book_repo: BookRepository = InMemoryBookRepository()
    user_repo: UserRepository = InMemoryUserRepository()
    create_user_use_case: CreateUserUseCase = CreateUserUseCase(user_repo)
    create_book_use_case: CreateBookUseCase = CreateBookUseCase(book_repo)
    return_book_use_case: ReturnBookUseCase = ReturnBookUseCase(book_repo, user_repo)
    borrow_book_use_case: BorrowBookUseCase = BorrowBookUseCase(book_repo, user_repo)
    return ReturnBookSetup(user_repo, book_repo, create_user_use_case, create_book_use_case, return_book_use_case, borrow_book_use_case)


def test_book_returned_succesfully(return_book_setup: ReturnBookSetup) -> None:
    book: Book = return_book_setup.create_book_use_case.run(CreateBookDTO(str(uuid4()), "mi libro", "gus"))
    user: User = return_book_setup.create_user_use_case.run(CreateUserDTO(str(uuid4()), "gus"))

    return_book_setup.borrow_book_use_case.run(user.id, book.id)
    old_reputation: Reputation = user.reputation
    
    return_book_setup.return_book_use_case.run(user.id, book.id)
    new_reputation: Reputation = user.reputation
    
    updated_user: Optional[User] = return_book_setup.user_repo.get_by_id(user.id)
    updated_book: Optional[Book] = return_book_setup.book_repo.get_by_id(book.id)
    
    assert updated_user is not None
    assert updated_book is not None
    
    assert len(updated_user.borrowed_books) == 0
    assert updated_book.availability
    assert new_reputation > old_reputation


def test_return_fails_if_user_does_not_have_the_book(return_book_setup: ReturnBookSetup) -> None:
    user: User = return_book_setup.create_user_use_case.run(CreateUserDTO(str(uuid4()), "gus"))
    book: Book = return_book_setup.create_book_use_case.run(CreateBookDTO(str(uuid4()), "mi libro", "gus"))
    
    with pytest.raises(UserDoesNotHaveTheBook):
        return_book_setup.return_book_use_case.run(user.id, book.id)


def test_return_fails_if_book_not_found(return_book_setup: ReturnBookSetup) -> None:
    user: User = return_book_setup.create_user_use_case.run(CreateUserDTO(str(uuid4()), "gus"))
    
    with pytest.raises(BookNotFound):
        return_book_setup.return_book_use_case.run(user.id, "")


def test_user_reputation_increase(return_book_setup: ReturnBookSetup) -> None:
    user: User = return_book_setup.create_user_use_case.run(CreateUserDTO(str(uuid4()), "gus"))
    user.reputation = user.reputation.increase(1)
    
    assert user.reputation == 3  # user reputation is 2 by default


def test_user_reputation_decrease(return_book_setup: ReturnBookSetup) -> None:
    user: User = return_book_setup.create_user_use_case.run(CreateUserDTO(str(uuid4()), "gus"))
    user.reputation = user.reputation.decrease(1)
    
    assert user.reputation == 1  # user reputation is 2 by default