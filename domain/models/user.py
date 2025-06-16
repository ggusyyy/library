from dataclasses import dataclass
from typing import List
from domain.models.book import Book
from domain.models.reputation import Reputation

@dataclass
class User:
    id: str
    name: str
    reputation: Reputation = Reputation(2)
    borrowed_books: List[Book] = []