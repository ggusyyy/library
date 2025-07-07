from uuid import uuid4
from typing import Optional
import pytest # type: ignore

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

def test_happy_path() -> None:
    user_repo: UserRepository = InMemoryUserRepository()
    book_repo: BookRepository = InMemoryBookRepository()
    
    create_user: CreateUserUseCase = CreateUserUseCase(user_repo)
    create_book: CreateBookUseCase = CreateBookUseCase(book_repo)
    
    return_book: ReturnBookUseCase = ReturnBookUseCase(book_repo, user_repo)
    borrow_book: BorrowBookUseCase = BorrowBookUseCase(book_repo, user_repo)
    
    book: Book = create_book.run(CreateBookDTO(str(uuid4()), "mi libro", "gus"))
    user: User = create_user.run(CreateUserDTO(str(uuid4()), "gus"))

    borrow_book.run(user.id, book.id)
    old_reputation: Reputation = user.reputation
    
    return_book.run(user.id, book.id)
    new_reputation: Reputation = user.reputation
    
    user_repo.update(user)
    book_repo.update(book)
    
    updated_user: Optional[User] = user_repo.get_by_id(user.id)
    updated_book: Optional[Book] = book_repo.get_by_id(book.id)
    
    assert updated_user is not None
    assert updated_book is not None
    
    assert len(updated_user.borrowed_books) == 0
    assert updated_book.availability
    assert new_reputation > old_reputation


def test_return_fails_if_user_does_not_have_the_book() -> None:
    user_repo: UserRepository = InMemoryUserRepository()
    book_repo: BookRepository = InMemoryBookRepository()
    
    create_user: CreateUserUseCase = CreateUserUseCase(user_repo)
    create_book: CreateBookUseCase = CreateBookUseCase(book_repo)
    return_book: ReturnBookUseCase = ReturnBookUseCase(book_repo, user_repo)
    
    user: User = create_user.run(CreateUserDTO(str(uuid4()), "gus"))
    book: Book = create_book.run(CreateBookDTO(str(uuid4()), "mi libro", "gus"))
    
    with pytest.raises(UserDoesNotHaveTheBook):
        return_book.run(user.id, book.id)


def test_return_fails_if_book_not_found() -> None:
    user_repo: UserRepository = InMemoryUserRepository()
    book_repo: BookRepository = InMemoryBookRepository()
    
    create_user: CreateUserUseCase = CreateUserUseCase(user_repo)
    return_book: ReturnBookUseCase = ReturnBookUseCase(book_repo, user_repo)
    
    user: User = create_user.run(CreateUserDTO(str(uuid4()), "gus"))
    
    with pytest.raises(BookNotFound):
        return_book.run(user.id, "")
        
def test_user_reputation_increase() -> None:
    user: User = User(str(uuid4()), "gus", Reputation(2))
    user.reputation = user.reputation.increase(1)
    
    assert user.reputation == 3


def test_user_reputation_decrease() -> None:
    user: User = User(str(uuid4()), "gus", Reputation(2))
    user.reputation = user.reputation.decrease(1)
    
    assert user.reputation == 1