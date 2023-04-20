using Infrastructure.Domains.Books.Models;

namespace Infrastructure.Domains.Books.Repositories
{
    public interface IBookRepository
    {
        public Book CreateBook(Book request);
        public void UpdateBook();
        public Book? GetBook(int id);
        public IEnumerable<Book> GetAllBooks();
        public void DeleteBook(Book book);
    }
}
