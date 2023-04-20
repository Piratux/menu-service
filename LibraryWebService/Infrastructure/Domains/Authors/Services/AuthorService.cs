using AutoMapper;
using Infrastructure.Domains.Authors.Models;
using Infrastructure.Domains.Authors.Repositories;

namespace Infrastructure.Domains.Authors.Services
{
    public class AuthorService : IAuthorService
    {
        private readonly IAuthorRepository _authorRepository;
        private readonly IMapper _mapper;
        public AuthorService(IAuthorRepository authorRepository, IMapper mapper)
        {
            _authorRepository = authorRepository;
            _mapper = mapper;
        }
        public CreateAuthorResponse CreateAuthor(AuthorRequest createRequest)
        {
            var author = _mapper.Map<Author>(createRequest);
            var newAuthor = _authorRepository.CreateAuthor(author);
            if (newAuthor == null)
            {
                return new CreateAuthorResponse("Failed to create author");
            }
            return new CreateAuthorResponse(author);
        }

        public DeleteAuthorResponse DeleteAuthor(int id)
        {
            var author = _authorRepository.GetAuthor(id);
            if (author == null)
            {
                return new DeleteAuthorResponse($"Author with id {id} doesn't exist", false);
            }
            _authorRepository.DeleteAuthor(author);
            return new DeleteAuthorResponse();
        }

        public IEnumerable<Author> GetAllAuthors()
        {
            return _authorRepository.GetAllAuthors();
        }

        public GetAuthorResponse GetAuthor(int id)
        {
            var author = _authorRepository.GetAuthor(id);
            if (author == null)
            {
                return new GetAuthorResponse($"Author with id {id} doesn't exist");
            }
            return new GetAuthorResponse(_mapper.Map<AuthorRequest>(author));
        }

        public UpdateAuthorResponse UpdateAuthor(int id, AuthorRequest updateRequest)
        {
            var author = _authorRepository.GetAuthor(id);
            if (author == null)
            {
                return new UpdateAuthorResponse($"Author with id {id} doesn't exist", false);
            }
            author.Name = updateRequest.Name;
            author.Surname = updateRequest.Surname;
            _authorRepository.UpdateAuthor();
            return new UpdateAuthorResponse(updateRequest);
        }
    }
}
