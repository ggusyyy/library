import sqlite3
from _sqlite3 import Cursor, Connection
from typing import Any, List, Optional

from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from infrastructure.repositories.user.queries import UserQueries as UQ


class SQLiteuserRepository(UserRepository):
    def __init__(self, db_path: str = "users.db") -> None:
        self.__conn: Connection = sqlite3.connect(db_path)
        self.__cursor: Cursor = self.__conn.cursor()
        
        self.__cursor.execute(UQ.CREATE_TABLE.value)
        self.__conn.commit()


    def commit_and_close(self) -> None:
        self.__conn.commit()
        self.__cursor.close()
  
  
    def is_table_empty(self) -> bool:
        self.__cursor.execute("SELECT * FROM users")
        return self.__cursor.fetchone() is None
    
    
    def save(self, user: User) -> None:
        if self.get_by_id(user.id) is None: 
            self.__cursor.execute(
                UQ.INSERT.value,
                (user.id, user.name, user.reputation)
                )
        else:
            self.update(user)
        self.commit_and_close()

    
    def get_all(self) -> List[User]:
        self.__cursor.execute(UQ.GET_ALL.value)
        rows: List[Any] = self.__cursor.fetchall()
        users: List[User] = [
            User(id=row[0], name=row[1], reputation=row[2])
            for row in rows
            ]
        self.commit_and_close()
        return users
    
    
    def get_by_id(self, id: str) -> Optional[User]:
        self.__cursor.execute(UQ.GET_BY_ID.value, (id,))
        row = self.__cursor.fetchone()
        if row:
            return User(id=row[0], name=row[1], reputation=row[2])
        self.__conn.commit()
        
    
    
    def update(self, user: User) -> None:
        self.__cursor.execute(
            UQ.UPDATE.value,
            (user.name, user.reputation, user.id)
            )
        self.commit_and_close()
    
    
    def delete(self, id: str) -> None:
        self.__cursor.execute(UQ.DELETE.value, (id,))
        self.commit_and_close()