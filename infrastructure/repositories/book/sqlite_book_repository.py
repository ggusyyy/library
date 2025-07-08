import sqlite3
from _sqlite3 import Cursor, Connection
from typing import Any, List, Optional

from domain.models.book import Book
from domain.repositories.book_repository import BookRepository
from infrastructure.repositories.book.queries import BookQueries as BQ


class SQLiteBookRepository(BookRepository):
    def __init__(self, db_path: str = "books.db") -> None:
        self.__conn: Connection = sqlite3.connect(db_path)
        
        self.__conn.execute(BQ.CREATE_TABLE.value)
        self.__conn.commit()
  
  
    def is_table_empty(self) -> bool:
        cursor: Cursor = self.__conn.execute("SELECT * FROM book")
        is_empty = cursor.fetchone() is None
        cursor.close()
        return is_empty
    
    
    def save(self, book: Book) -> None:
        if self.get_by_id(book.id) is None: 
            self.__conn.execute(
                BQ.INSERT.value,
                (book.id, book.title, book.author, book.availability)
                )
            self.__conn.commit()
        else:
            self.update(book)

    def get_all(self) -> List[Book]:
        cursor: Cursor = self.__conn.execute(BQ.GET_ALL.value)
        rows: list[Any] = cursor.fetchall()
        cursor.close()
        books: List[Book] = [
            Book(id=row[0], title=row[1], author=row[2], availability=bool(row[3]))
            for row in rows
            ]
        return books
    
    
    def get_by_id(self, id: str) -> Optional[Book]:
        cursor: Cursor = self.__conn.execute(BQ.GET_BY_ID.value, (id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Book(id=row[0], title=row[1], author=row[2], availability=bool(row[3]))
    
    
    def update(self, book: Book) -> None:
        self.__conn.execute(
            BQ.UPDATE.value,
            (book.title, book.author, book.availability, book.id)
            )
        self.__conn.commit()
    
    
    def delete(self, book_id: str) -> None:
        self.__conn.execute(BQ.DELETE.value, (book_id,))
        self.__conn.commit()
