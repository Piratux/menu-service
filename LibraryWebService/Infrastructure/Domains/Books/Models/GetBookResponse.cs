using Infrastructure.BaseModels;

namespace Infrastructure.Domains.Books.Models
{
    public class GetBookResponse : Response
    {
        public BookResponse? Book { get; private set; }
        public GetBookResponse(bool success, string? message, BookResponse? book) : base(success, message)
        {
            Book = book;
        }

        public GetBookResponse(string message) : this(false, message, null)
        {

        }
        public GetBookResponse(BookResponse book) : this(true, null, book)
        {

        }
    }
}
