using Infrastructure.BaseModels;

namespace Infrastructure.Domains.Books.Models
{
    public class DeleteBookResponse : Response
    {
        public bool Found { get; private set; }
        public DeleteBookResponse(bool success, string? message, bool found) : base(success, message)
        {
            Found = found;
        }

        public DeleteBookResponse() : this(true, null, true)
        {

        }

        public DeleteBookResponse(string message, bool found) : this(false, message, found)
        {

        }
    }
}
