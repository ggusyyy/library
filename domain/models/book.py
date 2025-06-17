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
    
    def change_availability(self, new_availability: bool) -> None:
        self.availability = new_availability
    
    def __repr__(self) -> str:
        return f"{self.title} - {self.author}"