import sqlite3
from _sqlite3 import Cursor, Connection
from typing import Any, List, Optional

from domain.models.book import Book
from domain.repositories.book_repository import BookRepository
from infrastructure.repositories.book.queries import BookQueries as BQ


class SQLiteBookRepository(BookRepository):
    def __init__(self, db_path: str = "library.db") -> None:
        self.__conn: Connection = sqlite3.connect(db_path)
        self.__cursor: Cursor = self.__conn.cursor()
        
        self.__cursor.execute(BQ.CREATE_TABLE.value)
        self.__conn.commit()


    def commit_and_close(self) -> None:
        self.__conn.commit()
        self.__cursor.close()
  
  
    def is_table_empty(self) -> bool:
        self.__cursor.execute("SELECT * FROM book")
        return self.__cursor.fetchone() is None
    
    
    def save(self, book: Book) -> None:
        if self.get_by_id(book.id) is None: 
            self.__cursor.execute(
                BQ.INSERT.value,
                (book.id, book.title, book.author, book.availability)
                )
        else:
            self.update(book)
        self.commit_and_close()

    def get_all(self) -> List[Book]:
        self.__cursor.execute(BQ.GET_ALL.value)
        rows: list[Any] = self.__cursor.fetchall()
        books: List[Book] = [
            Book(id=row[0], title=row[1], author=row[2], availability=bool(row[3]))
            for row in rows
            ]
        self.commit_and_close()
        return books
    
    
    def get_by_id(self, id: str) -> Optional[Book]:
        self.__cursor.execute(BQ.GET_BY_ID.value, (id,))
        row = self.__cursor.fetchone()
        if row:
            return Book(id=row[0], title=row[1], author=row[2], availability=bool(row[3]))
        self.__conn.commit()
        
    
    
    def update(self, book: Book) -> None:
        self.__cursor.execute(
            BQ.UPDATE.value,
            (book.title, book.author, book.availability, book.id)
            )
        self.commit_and_close()
    
    
    def delete(self, book_id: str) -> None:
        self.__cursor.execute(BQ.DELETE.value, (book_id,))
        self.commit_and_close()