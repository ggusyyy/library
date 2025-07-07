from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Reputation:
    reputation: int
    
    def __repr__(self) -> str:
        return str(self.reputation)
    
    def __gt__(self, other: Any) -> bool:
        if isinstance(other, Reputation):
            return self.reputation > other.reputation
        return NotImplemented
    
    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Reputation):
            return self.reputation < other.reputation
        return NotImplemented
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Reputation):
            return self.reputation == other.reputation
        elif isinstance(other, int):
            return self.reputation == other
        return NotImplemented

    
    def increase(self, amount: int) -> "Reputation":
         return Reputation(self.reputation + amount)
        
    def decrease(self, amount: int) -> "Reputation":
        return Reputation(max(0, self.reputation - amount))