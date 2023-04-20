using Infrastructure.Domains.Authors.Models;
using Infrastructure.Repositories;

namespace Infrastructure.Domains.Authors.Repositories
{
    public class AuthorRepository : IAuthorRepository
    {

        private readonly RepositoryContext _context;

        public AuthorRepository(RepositoryContext context)
        {
            _context = context;
        }

        public Author CreateAuthor(Author request)
        {
            var author = _context.Author.Add(request);
            _context.SaveChanges();
            return author.Entity;
        }

        public void DeleteAuthor(Author author)
        {
            _context.Author.Remove(author);
            _context.SaveChanges();
        }

        public IEnumerable<Author> GetAllAuthors()
        {
            return _context.Author;
        }

        public Author? GetAuthor(int id)
        {
            var authors = GetAllAuthors();
            return authors.Where(x => x.Id == id).FirstOrDefault();
        }

        public void UpdateAuthor()
        {
            _context.SaveChanges();
        }
    }
}
