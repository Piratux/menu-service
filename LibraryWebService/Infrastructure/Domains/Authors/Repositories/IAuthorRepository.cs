using Infrastructure.Domains.Authors.Models;

namespace Infrastructure.Domains.Authors.Repositories
{
    public interface IAuthorRepository
    {
        public Author CreateAuthor(Author request);
        public void UpdateAuthor();
        public Author? GetAuthor(int id);
        public IEnumerable<Author> GetAllAuthors();
        public void DeleteAuthor(Author author);
    }
}
