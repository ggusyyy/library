from dataclasses import dataclass


@dataclass
class CreateBookDTO:
    id: str
    title: str
    author: str
    availability: bool = True