using Infrastructure.BaseModels;

namespace Infrastructure.Domains.Authors.Models
{
    public class UpdateAuthorResponse : Response
    {
        public bool Found { get; private set; }
        public AuthorRequest? Author { get; set; }
        public UpdateAuthorResponse(bool success, AuthorRequest? author, string message, bool found) : base(success, message)
        {
            Found = found;
            Author = author;
        }

        public UpdateAuthorResponse(AuthorRequest? author) : this(true, author, null, true)
        {

        }

        public UpdateAuthorResponse(string message, bool found) : this(false, null, message, found)
        {

        }
    }
}
