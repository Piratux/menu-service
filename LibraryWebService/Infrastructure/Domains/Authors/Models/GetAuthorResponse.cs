using Infrastructure.BaseModels;

namespace Infrastructure.Domains.Authors.Models
{
    public class GetAuthorResponse : Response
    {
        public AuthorRequest? Author { get; set; }
        public GetAuthorResponse(bool success, string? message, AuthorRequest? author) : base(success, message)
        {
            Author = author;
        }

        public GetAuthorResponse(AuthorRequest? author) : this(true, null, author)
        {
            
        }

        public GetAuthorResponse(string message) : this(false, message, null)
        {
            
        }
    }
}
