from typing import Optional

from domain.exceptions.book_not_found import BookNotFound
from domain.exceptions.user_does_not_have_the_book import UserDoesNotHaveTheBook
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
        self.__book_repository: BookRepository = book_repository
        self.__user_repository: UserRepository = user_repository
    
    def run(self, user_id: str, book_id: str) -> None:
        user: Optional[User] = self.__user_repository.get_by_id(user_id)
        if not user:
            raise UserNotRegistered()
        
        book: Optional[Book] = self.__book_repository.get_by_id(book_id)
        if not book:
            raise BookNotFound()
          
        if book not in user.borrowed_books:
            raise UserDoesNotHaveTheBook()
        
        user.return_book(book.id)
        user.reputation.increase(1)
        book.change_availability(True)
        
        self.__user_repository.update(user)
        self.__book_repository.update(book)