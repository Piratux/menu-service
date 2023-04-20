using Infrastructure.BaseModels;

namespace Infrastructure.Domains.Authors.Models
{
    public class CreateAuthorResponse : Response
    {
        public Author? Author { get; private set; }

        public CreateAuthorResponse(bool success, string? message, Author? author) : base(success, message)
        {
            Author = author;
        }

        public CreateAuthorResponse(string? message) : this(false, message, null)
        {
        }

        public CreateAuthorResponse(Author? author) : this(true, null, author)
        {
        }
    }
}
