from dataclasses import dataclass


@dataclass
class CreateUserDTO:
    id: str
    name: str