from dataclasses import dataclass

@dataclass
class Reputation:
    reputation: int
    
    def __repr__(self) -> str:
        return str(self.reputation)
    
    def increase(self, amount: int) -> None:
        self.reputation += amount
        
    def decrease(self, amount: int) -> None:
        self.reputation = max(0, self.reputation - amount)