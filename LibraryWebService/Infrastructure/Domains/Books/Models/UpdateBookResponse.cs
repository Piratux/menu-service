using Infrastructure.BaseModels;

namespace Infrastructure.Domains.Books.Models
{
    public class UpdateBookResponse : Response
    {
        public bool Found { get; private set; }
        public BookRequest? Book { get; set; }
        public UpdateBookResponse(bool success, BookRequest? book, string message, bool found) : base(success, message)
        {
            Found = found;
            Book = book;
        }

        public UpdateBookResponse(BookRequest book) : this(true, book, null!, true)
        {

        }

        public UpdateBookResponse(string message, bool found) : this(false, null, message, found)
        {

        }
    }
}
