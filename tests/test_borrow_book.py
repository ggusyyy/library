from typing import List, Optional
from uuid import uuid4
import pytest

from domain.exceptions.book_not_available import BookNotAvailable
from domain.exceptions.book_not_found import BookNotFound
from domain.exceptions.user_cant_borrow_more import UserCantBorrowMore
from domain.exceptions.user_not_registered import UserNotRegistered
from domain.models.book import Book
from domain.models.user import User
from domain.repositories.book_repository import BookRepository
from domain.repositories.user_repository import UserRepository

from application.dtos.create_book import CreateBookDTO
from application.dtos.create_user import CreateUserDTO
from application.use_cases.create_book import CreateBookUseCase
from application.use_cases.create_user import CreateUserUseCase
from application.use_cases.borrow_book import BorrowBookUseCase

from infrastructure.repositories.book.in_memory_book_repository import InMemoryBookRepository
from infrastructure.repositories.user.in_memory_user_repository import InMemoryUserRepository


def test_happy_path() -> None:
    user_repo: UserRepository = InMemoryUserRepository()
    book_repo: BookRepository = InMemoryBookRepository()
    
    create_user = CreateUserUseCase(user_repo)
    create_book = CreateBookUseCase(book_repo)
    borrow_book = BorrowBookUseCase(book_repo, user_repo)
    
    user: User = create_user.run(CreateUserDTO(str(uuid4()), "gus"))
    book: Book = create_book.run(CreateBookDTO(str(uuid4()), "mi_libro", "gus"))
    
    borrow_book.run(user.id, book.id)
    
    user_repo.update(user)
    book_repo.update(book)
    
    updated_user: Optional[User] = user_repo.get_by_id(user.id)
    updated_book: Optional[Book] = book_repo.get_by_id(book.id)
    
    assert updated_user is not None
    assert updated_book is not None
    
    assert len(updated_user.borrowed_books) == 1
    assert updated_book.availability is False

    
def test_borrow_fails_if_book_not_found() -> None:
    user_repo: UserRepository = InMemoryUserRepository()
    book_repo: BookRepository = InMemoryBookRepository()
    
    create_user = CreateUserUseCase(user_repo)
    borrow_book = BorrowBookUseCase(book_repo, user_repo)
    
    user: User = create_user.run(CreateUserDTO(str(uuid4()), "gus"))
    
    with pytest.raises(BookNotFound):
        borrow_book.run(user.id, "")
        

def test_borrow_fails_if_boot_not_available() -> None:
    user_repo: UserRepository = InMemoryUserRepository()
    book_repo: BookRepository = InMemoryBookRepository()
    
    create_user: CreateUserUseCase = CreateUserUseCase(user_repo)
    create_book: CreateBookUseCase = CreateBookUseCase(book_repo)
    borrow_book: BorrowBookUseCase = BorrowBookUseCase(book_repo, user_repo)
    
    user: User = create_user.run(CreateUserDTO(str(uuid4()), "gus"))
    book: Book = create_book.run(CreateBookDTO(str(uuid4()), "mi libro", "gus", False))
    
    with pytest.raises(BookNotAvailable):
        borrow_book.run(user.id, book.id)


def test_borrow_fails_if_user_not_registered() -> None:
    user_repo: UserRepository = InMemoryUserRepository()
    book_repo: BookRepository = InMemoryBookRepository()
    
    create_book = CreateBookUseCase(book_repo)
    borrow_book = BorrowBookUseCase(book_repo, user_repo)
    
    book: Book = create_book.run(CreateBookDTO(str(uuid4()), "mi_libro", "gus"))
    
    with pytest.raises(UserNotRegistered):
        borrow_book.run("", book.id)

        
def test_borrow_fails_if_user_cant_borrow_more() -> None:
    user_repo: UserRepository = InMemoryUserRepository()
    book_repo: BookRepository = InMemoryBookRepository()
    
    create_user: CreateUserUseCase = CreateUserUseCase(user_repo)
    create_book: CreateBookUseCase = CreateBookUseCase(book_repo)
    borrow_book: BorrowBookUseCase = BorrowBookUseCase(book_repo, user_repo)
        
    user: User = create_user.run(CreateUserDTO(str(uuid4()), "gus"))
    
    books: List[Book] = [
        create_book.run(CreateBookDTO(str(uuid4()), "mi libro 1", "gus 1")), 
        create_book.run(CreateBookDTO(str(uuid4()), "mi libro 2", "gus 2")),
        create_book.run(CreateBookDTO(str(uuid4()), "mi libro 3", "gus 3")),
        create_book.run(CreateBookDTO(str(uuid4()), "mi libro 4", "gus 4")),
        create_book.run(CreateBookDTO(str(uuid4()), "mi libro 5", "gus 5")),
        create_book.run(CreateBookDTO(str(uuid4()), "mi libro 6", "gus 6"))
    ]
    
    borrow_book.run(user.id, books[0].id)
    borrow_book.run(user.id, books[1].id)
    borrow_book.run(user.id, books[2].id)
    borrow_book.run(user.id, books[3].id)
    borrow_book.run(user.id, books[4].id)
    
    with pytest.raises(UserCantBorrowMore):
        borrow_book.run(user.id, books[5].id)