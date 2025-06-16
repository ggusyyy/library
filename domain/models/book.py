from  dataclasses import dataclass

@dataclass
class Book:
    id: str
    title: str
    author: str
    availability: bool = True
    
    @property
    def is_available(self) -> bool:
        return self.availability
    
    def change_availability(self) -> None:
        self.availability = False