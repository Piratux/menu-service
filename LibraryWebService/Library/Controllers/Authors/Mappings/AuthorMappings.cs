using AutoMapper;
using Infrastructure.Domains.Authors.Models;

namespace Library.API.Controllers.Authors.Mappings
{
    public class AuthorMappings : Profile
    {
        public AuthorMappings()
        {
            CreateMap<Author, AuthorRequest>().ReverseMap();
        }
    }
}
