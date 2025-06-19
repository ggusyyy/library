from uuid import uuid4

from application.dtos.create_book import CreateBookDTO
from application.dtos.create_user import CreateUserDTO
from application.use_cases.borrow_book import BorrowBookUseCase
from application.use_cases.create_book import CreateBookUseCase
from application.use_cases.create_user import CreateUserUseCase

from domain.repositories.book_repository import BookRepository
from domain.repositories.user_repository import UserRepository

from infrastructure.repositories.book.in_memory_book_repository import InMemoryBookRepository
from infrastructure.repositories.user.in_memory_user_repository import InMemoryUserRepository


def main() -> None:
    print("\n")
    
    user_repo: UserRepository = InMemoryUserRepository()
    book_repo: BookRepository = InMemoryBookRepository()

    create_user: CreateUserUseCase = CreateUserUseCase(user_repo)
    create_book: CreateBookUseCase = CreateBookUseCase(book_repo)
    borrow_book: BorrowBookUseCase = BorrowBookUseCase(book_repo, user_repo)
    
    gus = create_user.run(CreateUserDTO(str(uuid4()), "Gus"))
    gus_book = create_book.run(CreateBookDTO(str(uuid4()), "Libro de Gus", gus.name))
    
    user_repo.save(gus)
    book_repo.save(gus_book)
    
    borrow_book.run(gus.id, gus_book.id)
    
    print(gus.borrowed_books)
    print(gus_book.is_available)
    
    

if __name__ == "__main__":
    main()