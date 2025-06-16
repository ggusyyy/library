from typing import Dict, List, Optional

from domain.models.user import User
from domain.repositories.user_repository import UserRepository

class InMemoryUserRepository(UserRepository):
    
    def __init__(self) -> None:
        self.users: Dict[str, User]
    
    
    def save(self, user: User) -> None:
        self.users[user.id] = User
    
    
    def get_all(self) -> List[User]:
        return self.users

    
    def get_by_id(self, id: str) -> Optional[User]:
        for user in self.users:
            if user.id == id:
                return user


    def update(self, user):
        self.save(user)
    
    
    def delete(self, id: str) -> None:
        for user in self.users:
            if user.id == id:
                self.users.pop(user.id)