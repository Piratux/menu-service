using Infrastructure.BaseModels;

namespace Infrastructure.Domains.Authors.Models
{
    public class DeleteAuthorResponse : Response
    {
        public bool Found { get; private set; }
        public DeleteAuthorResponse(bool success, string? message, bool found) : base(success, message)
        {
            Found = found;
        }

        public DeleteAuthorResponse() : this(true, null, true)
        {
        }

        public DeleteAuthorResponse(string? message, bool found) : this(false, message, found)
        {
        }
    }
}
