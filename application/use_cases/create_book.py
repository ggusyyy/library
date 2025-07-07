from application.dtos.create_book import CreateBookDTO
from domain.exceptions.book_already_exists import BookAlreadyExists
from domain.models.book import Book

from domain.repositories.book_repository import BookRepository


class CreateBookUseCase:
    def __init__(self, book_repository: BookRepository,) -> None:
        self.__book_repository: BookRepository = book_repository
    
    def run(self, input: CreateBookDTO) -> Book:
        if self.__book_repository.get_by_id(input.id):
            raise BookAlreadyExists()
        
        book: Book = Book(input.id, input.title, input.author, input.availability)
        self.__book_repository.save(book)
        return book