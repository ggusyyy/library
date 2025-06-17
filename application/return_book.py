from typing import Optional

from domain.exceptions.book_not_found import BookNotFound
from domain.exceptions.user_not_registered import UserNotRegistered
from domain.models.book import Book
from domain.models.user import User
from domain.repositories.book_repository import BookRepository
from domain.repositories.user_repository import UserRepository


class ReturnBookUseCase:
    def __init__(
        self,
        book_repository: BookRepository,
        user_repository: UserRepository
        ) -> None:
        self.book_repository: BookRepository = book_repository
        self.user_repository: UserRepository = user_repository
    
    def run(self, user_id: str, book_id: str) -> None:
        user: Optional[User] = self.user_repository.get_by_id(user_id)
        book: Optional[Book] = self.book_repository.get_by_id(book_id)
        
        if not user:
            raise UserNotRegistered()
        
        if not book:
            raise BookNotFound()
        
        user.return_book(book.id)
        book.change_availability(True)
        
        self.user_repository.save(user)
        self.book_repository.save(book)