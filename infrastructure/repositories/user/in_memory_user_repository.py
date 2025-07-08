from typing import List, Optional

from domain.models.user import User
from domain.repositories.user_repository import UserRepository

class InMemoryUserRepository(UserRepository):
    
    def __init__(self) -> None:
        self.__users: List[User] = []
    
    
    def save(self, user: User) -> None:
        if self.get_by_id(user.id) is None:    
            self.__users.append(user)
            return
        self.update(user)
    
    
    def get_all(self) -> List[User]:
        return [user for user in self.__users]

    
    def get_by_id(self, id: str) -> Optional[User]:
        for user in self.__users:
            if user.id == id:
                return user
        return None


    def update(self, user: User):
        for index, stored_user in enumerate(self.__users):
            if stored_user.id == user.id:
                self.__users[index] = user
                break
    
    
    def delete(self, id: str) -> None:
        self.__users = [user for user in self.__users if user.id != id]