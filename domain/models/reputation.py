from dataclasses import dataclass

@dataclass(frozen=True)
class Reputation:
    reputation: int
    
    def __repr__(self) -> str:
        return str(self.reputation)
    
    def increase(self, amount: int) -> "Reputation":
         return Reputation(self.reputation + amount)
        
    def decrease(self, amount: int) -> "Reputation":
        return Reputation(max(0, self.reputation - amount))