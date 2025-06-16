from typing import Dict, List, Optional

from domain.models.book import Book
from domain.repositories.book_repository import BookRepository

class InMemoryBookRepository(BookRepository):
    
    def __init__(self) -> None:
        self.books: Dict[str, Book]
    
    
    def save(self, book: Book) -> None:
        self.books[book.id] = Book
    
    
    def get_all(self) -> List[Book]:
        return self.books


    def get_by_id(self, id: str) -> Optional[Book]:
        for book in self.books:
            if book.id == id:
                return book


    def update(self, book):
        self.save(book)
    
    
    def delete(self, id: str) -> None:
        for book in self.books:
            if book.id == id:
                self.books.pop(book.id)