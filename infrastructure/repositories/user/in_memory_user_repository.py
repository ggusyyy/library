from typing import List, Optional

from domain.exceptions.user_not_registered import UserNotRegistered
from domain.models.user import User
from domain.repositories.user_repository import UserRepository

class InMemoryUserRepository(UserRepository):
    
    def __init__(self) -> None:
        self.__users: List[User] = []
    
    
    def save(self, user: User) -> None:
        if self.get_by_id(user.id) is None:    
            self.__users.append(user)
            return
        for index, stored_user in enumerate(self.__users):
            if stored_user.id == user.id:
                self.__users[index] = user
    
    
    def get_all(self) -> List[User]:
        return self.__users

    
    def get_by_id(self, id: str) -> Optional[User]:
        for user in self.__users:
            if user.id == id:
                return user


    def update(self, user: User):
        if not self.get_by_id(user.id):    
            raise UserNotRegistered()
        
        for index, stored_user in enumerate(self.__users):
            if stored_user.id == user.id:
                self.__users[index] = user
    
    
    def delete(self, id: str) -> None:
        for user in self.__users:
            if user.id == id:
                self.__users.remove(user)