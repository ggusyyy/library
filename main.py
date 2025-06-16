from uuid import uuid4
from application.borrow_book import BorrowBookUseCase
from domain.models.book import Book
from domain.models.user import User
from domain.repositories.book_repository import BookRepository
from domain.repositories.user_repository import UserRepository
from infrastructure.repositories.book.in_memory_book_repository import InMemoryBookRepository
from infrastructure.repositories.user.in_memory_user_repository import InMemoryUserRepository


def main() -> None:
    user_repo: UserRepository = InMemoryUserRepository()
    book_repo: BookRepository = InMemoryBookRepository()
    
    user: User = User(str(uuid4), "Gus")
    book: Book = Book(str(uuid4), "Mi Libro", "Yo")
    
    user_repo.save(user)
    book_repo.save(book)
    
    borrow_book_use_case: BorrowBookUseCase = BorrowBookUseCase(book_repo, user_repo)
    borrow_book_use_case.run(user.id, book.id)

if __name__ == "__main__":
    main()