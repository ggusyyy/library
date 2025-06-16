from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.user import User

class BookRepository(ABC):
    @abstractmethod
    def save(self, book: User) -> None: ...

    @abstractmethod
    def get_all(self) -> List[User]: ...

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[User]: ...

    @abstractmethod
    def delete(self, id: str) -> None: ...