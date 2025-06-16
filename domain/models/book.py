from  dataclasses import dataclass

@dataclass
class Book:
    id: str
    title: str
    author: str
    availability: bool