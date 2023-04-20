using Infrastructure.BaseModels;

namespace Infrastructure.Domains.Books.Models
{
    public class CreateBookResponse : Response
    {
        public Book? Book { get; private set; }
        public CreateBookResponse(bool success, string? message, Book? book) : base(success, message)
        {
            Book = book;
        }

        public CreateBookResponse(Book book) : this(true, null, book)
        {

        }
        public CreateBookResponse(string message) : this(false, message, null)
        {

        }

    }
}
