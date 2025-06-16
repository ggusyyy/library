from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.user import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None: ...

    @abstractmethod
    def get_all(self) -> List[User]: ...

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[User]: ...

    @abstractmethod
    def update(self, user: User) -> None: ...
    
    @abstractmethod
    def delete(self, id: str) -> None: ...