from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.book import Book

class BookRepository(ABC):
    @abstractmethod
    def save(self, book: Book) -> None: ...

    @abstractmethod
    def get_all(self) -> List[Book]: ...

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Book]: ...

    @abstractmethod
    def update(self, book: Book) -> None: ...
    
    @abstractmethod
    def delete(self, book_id: str) -> None: ...