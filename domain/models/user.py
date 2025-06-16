from dataclasses import dataclass, field
from typing import List
from domain.exceptions.book_not_available import BookNotAvailable
from domain.models.book import Book
from domain.models.reputation import Reputation

@dataclass
class User:
    id: str
    name: str
    reputation: Reputation = Reputation(2)
    borrowed_books: List[Book] = field(default_factory=list[Book])
    
    def borrow_book(self, book: Book) -> None:
        if not book.is_available:
            raise BookNotAvailable
        
        self.borrowed_books.append(book)
    
    def remove_borrowed_book(self, book_id: str) -> None:
        for book in self.borrowed_books:
            if book.id == book_id:
                self.borrowed_books.remove(book)