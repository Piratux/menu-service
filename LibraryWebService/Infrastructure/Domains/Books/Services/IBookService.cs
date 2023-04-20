using Infrastructure.Domains.Books.Models;

namespace Infrastructure.Domains.Books.Services
{
    public interface IBookService
    {
        public CreateBookResponse CreateBook(BookRequest createRequest);

        public GetBookResponse GetBook(int id);

        public IEnumerable<Book> GetAllBooks();

        public UpdateBookResponse UpdateBook(int id, BookRequest updateRequest);

        public DeleteBookResponse DeleteBook(int id);

    }
}
