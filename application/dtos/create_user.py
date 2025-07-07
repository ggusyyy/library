from dataclasses import dataclass, field
from typing import List

from domain.models.book import Book


@dataclass
class CreateUserDTO:
    id: str
    name: str
    borrowed_books: List[Book] = field(default_factory=list[Book])