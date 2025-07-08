from enum import Enum

class UserQueries(Enum):
    CREATE_TABLE = """CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                reputation INTEGER NOT NULL
            );"""
    INSERT = "INSERT INTO users (id, name, reputation) VALUES (?, ?, ?);"
    GET_ALL = "SELECT * FROM users;"
    GET_BY_ID = "SELECT * FROM users WHERE id = ?;"
    UPDATE = "UPDATE users SET name = ?, reputation = ? WHERE id = ?;"
    DELETE = "DELETE FROM users WHERE id = ?;"