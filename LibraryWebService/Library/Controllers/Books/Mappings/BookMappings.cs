using AutoMapper;
using Infrastructure.Domains.Books.Models;

namespace Library.Controllers.Books.Mappings
{
    public class BookMappings : Profile
    {
        public BookMappings()
        {
            CreateMap<Book, BookRequest>().ReverseMap();
            CreateMap<Book, BookResponse>().ReverseMap();
        }
    }
}
