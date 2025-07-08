import sqlite3
from _sqlite3 import Cursor, Connection
from typing import Any, List, Optional

from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from infrastructure.repositories.user.queries import UserQueries as UQ


class SQLiteuserRepository(UserRepository):
    def __init__(self, db_path: str = "users.db") -> None:
        self.__conn: Connection = sqlite3.connect(db_path)
        cursor: Cursor = self.__conn.cursor()
        
        cursor.execute(UQ.CREATE_TABLE.value)
        self.__conn.commit()
        cursor.close()
  
    def is_table_empty(self) -> bool:
        cursor: Cursor = self.__conn.execute("SELECT * FROM users")
        is_empty = cursor.fetchone() is None
        cursor.close()
        return is_empty
    
    
    def save(self, user: User) -> None:
        if self.get_by_id(user.id) is None: 
            self.__conn.execute(
                UQ.INSERT.value,
                (user.id, user.name, user.reputation)
                )
            self.__conn.commit()
        else:
            self.update(user)

    
    def get_all(self) -> List[User]:
        cursor: Cursor = self.__conn.execute(UQ.GET_ALL.value)
        rows: List[Any] = cursor.fetchall()
        cursor.close()
        users: List[User] = [
            User(id=row[0], name=row[1], reputation=row[2])
            for row in rows
            ]
        return users
    
    
    def get_by_id(self, id: str) -> Optional[User]:
        cursor: Cursor = self.__conn.execute(UQ.GET_BY_ID.value, (id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return User(id=row[0], name=row[1], reputation=row[2])
        self.__conn.commit()
        
    
    
    def update(self, user: User) -> None:
        self.__conn.execute(
            UQ.UPDATE.value,
            (user.name, user.reputation, user.id)
            )
        self.__conn.commit()
    
    
    def delete(self, id: str) -> None:
        self.__conn.execute(UQ.DELETE.value, (id,))
        self.__conn.commit()