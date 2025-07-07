from dataclasses import dataclass
from uuid import uuid4

import pytest

from application.dtos.create_book import CreateBookDTO
from application.use_cases.create_book import CreateBookUseCase
from domain.exceptions.book_already_exists import BookAlreadyExists
from domain.models.book import Book
from domain.repositories.book_repository import BookRepository
from infrastructure.repositories.book.in_memory_book_repository import InMemoryBookRepository


@dataclass
class CreateBookSetup: ...

def test_book_created_succesfully() -> None:
    repo: BookRepository = InMemoryBookRepository()
    create_book: CreateBookUseCase = CreateBookUseCase(repo)
    gus: Book = create_book.run(CreateBookDTO(str(uuid4()), "mi libro", "gus"))
    
    assert isinstance(gus, Book)
    assert gus.title == "mi libro"
    assert gus.author == "gus"
    assert gus.id is not None
    
def test_book_cannot_be_created_if_already_exists() -> None:
    repo: BookRepository = InMemoryBookRepository()
    create_book: CreateBookUseCase = CreateBookUseCase(repo)
    gus: Book = create_book.run(CreateBookDTO(str(uuid4()), "mi libro", "gus"))
    
    with pytest.raises(BookAlreadyExists):
        create_book.run(CreateBookDTO(gus.id, "mi libro", "gus"))