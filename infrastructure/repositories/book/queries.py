from enum import Enum


class BookQueries(Enum):
    CREATE_TABLE = """CREATE TABLE IF NOT EXISTS books (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                availability INTEGER NOT NULL CHECK (availability IN (0, 1))
            );"""
    INSERT = "INSERT INTO books (id, title, author, availability) VALUES (?, ?, ?, ?);"
    GET_ALL = "SELECT * FROM books;"
    GET_BY_ID = "SELECT * FROM books WHERE id = ?;"
    UPDATE = "UPDATE books SET title = ?, author = ?, availability = ? WHERE id = ?;"
    DELETE = "DELETE FROM books WHERE id = ?;"