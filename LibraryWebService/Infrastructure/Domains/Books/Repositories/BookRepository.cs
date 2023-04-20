using Infrastructure.Domains.Books.Models;
using Infrastructure.Repositories;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Domains.Books.Repositories
{
    public class BookRepository : IBookRepository
    {
        private readonly RepositoryContext _context;

        public BookRepository(RepositoryContext context)
        {
            _context = context;
        }
        public Book CreateBook(Book request)
        {
            var book = _context.Books.Add(request);
            _context.SaveChanges();
            return book.Entity;
        }

        public void DeleteBook(Book book)
        {
            _context.Books.Remove(book);
            _context.SaveChanges();
        }

        public IEnumerable<Book> GetAllBooks()
        {
            return _context.Books.Include("Author");
        }

        public Book? GetBook(int id)
        {
            var books = GetAllBooks();
            return GetAllBooks().Where(x => x.Id == id).FirstOrDefault();
        }

        public void UpdateBook()
        {
            _context.SaveChanges();
        }
    }
}
