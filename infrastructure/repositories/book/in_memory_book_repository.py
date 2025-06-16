from typing import List, Optional

from domain.exceptions.book_not_found import BookNotFound
from domain.models.book import Book
from domain.repositories.book_repository import BookRepository

class InMemoryBookRepository(BookRepository):
    
    def __init__(self) -> None:
        self.books: List[Book] = []
    
    
    def save(self, book: Book) -> None:
        if self.get_by_id(book.id) is None:    
            self.books.append(book)
            return
        self.update(book)
    
    
    def get_all(self) -> List[Book]:
        return self.books


    def get_by_id(self, id: str) -> Optional[Book]:
        for book in self.books:
            if book.id == id:
                return book


    def update(self, book: Book) -> None:
        if not self.get_by_id(book.id):    
            raise BookNotFound()
        
        for index, stored_book in enumerate(self.books):
            if stored_book.id == book.id:
                self.books[index] = book
        
    
    
    def delete(self, book_id: str) -> None:
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)