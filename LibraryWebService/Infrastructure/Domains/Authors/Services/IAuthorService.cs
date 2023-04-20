using Infrastructure.Domains.Authors.Models;

namespace Infrastructure.Domains.Authors.Services
{
    public interface IAuthorService
    {
        public CreateAuthorResponse CreateAuthor(AuthorRequest createRequest);

        public GetAuthorResponse GetAuthor(int id);

        public IEnumerable<Author> GetAllAuthors();

        public UpdateAuthorResponse UpdateAuthor(int id, AuthorRequest updateRequest);

        public DeleteAuthorResponse DeleteAuthor(int id);
    }
}
