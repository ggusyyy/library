from dataclasses import dataclass, field
from typing import List
from domain.exceptions.book_not_available import BookNotAvailable
from domain.exceptions.user_cant_borrow_more import UserCantBorrowMore
from domain.models.book import Book
from domain.models.reputation import Reputation

@dataclass
class User:
    id: str
    name: str
    reputation: Reputation = Reputation(2)
    borrowed_books: List[Book] = field(default_factory=list[Book])
    
    def __repr__(self) -> str:
        return self.name
    
    
    def borrow_book(self, book: Book) -> None:
        if not book.is_available:
            raise BookNotAvailable
        
        if not self.can_borrow_more():
            raise UserCantBorrowMore()
        
        self.borrowed_books.append(book)
    
    
    def return_book(self, book_id: str) -> None:
        for book in self.borrowed_books:
            if book.id == book_id:
                self.borrowed_books.remove(book)
        self.reputation.increase(1)
    
    
    def can_borrow_more(self) -> bool:
        return not len(self.borrowed_books) > 5