from uuid import uuid4
from application.return_book import ReturnBookUseCase
from domain.models.book import Book
from domain.models.user import User
from domain.repositories.book_repository import BookRepository
from domain.repositories.user_repository import UserRepository
from infrastructure.repositories.book.in_memory_book_repository import InMemoryBookRepository
from infrastructure.repositories.user.in_memory_user_repository import InMemoryUserRepository


def main() -> None:
    print("\n")
    
    user_repo: UserRepository = InMemoryUserRepository()
    book_repo: BookRepository = InMemoryBookRepository()
    
    user: User = User(str(uuid4), "Gus")
    book: Book = Book(str(uuid4), "Mi Libro", "Yo")
    
    user_repo.save(user)
    book_repo.save(book)
    
    return_book_use_case: ReturnBookUseCase = ReturnBookUseCase(book_repo, user_repo)
    return_book_use_case.run(user.id, book.id)
    
    print(user.borrowed_books)
    print(user.reputation)
    print(book.is_available)
    

if __name__ == "__main__":
    main()