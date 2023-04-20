using Infrastructure.Domains.Books.Models;
using Infrastructure.Domains.Books.Services;
using Library.Extensions;
using Microsoft.AspNetCore.Mvc;
using Swashbuckle.AspNetCore.Annotations;

namespace Library.Controllers.Books
{
    [ApiController]
    [Route("api/[controller]")]
    public class BooksController : ControllerBase
    {

        private readonly IBookService _bookService;

        public BooksController(IBookService service)
        {
            _bookService = service;
        }

        [HttpGet]
        [SwaggerOperation(Summary = "Returns all books")]
        [ApiConventionMethod(typeof(DefaultApiConventions), nameof(DefaultApiConventions.Get))]
        public IActionResult GetAllBooks()
        {
            return Ok(_bookService.GetAllBooks());
        }


        [HttpGet("{id}")]
        [SwaggerOperation(Summary = "Returns book by id")]
        [ApiConventionMethod(typeof(DefaultApiConventions), nameof(DefaultApiConventions.Get))]
        public IActionResult GetBook(int id)
        {
            var bookReponse = _bookService.GetBook(id);

            if (!bookReponse.Success)
            {
                return NotFound(bookReponse.Message);
            }
            return Ok(bookReponse.Book);
        }

        [HttpPost]
        [SwaggerOperation(Summary = "Creates new book from request")]
        [ApiConventionMethod(typeof(DefaultApiConventions), nameof(DefaultApiConventions.Post))]
        public IActionResult CreateBook([FromBody] BookRequest request)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var bookResponse = _bookService.CreateBook(request);

            if (!bookResponse.Success)
            {
                return BadRequest(bookResponse.Message);
            }

            return CreatedAtAction(nameof(GetBook), new { id = bookResponse.Book?.Id }, bookResponse.Book);
        }

        [HttpPut("{id}")]
        [SwaggerOperation(Summary = "Updates book with id")]
        [ApiConventionMethod(typeof(DefaultApiConventions), nameof(DefaultApiConventions.Put))]
        public IActionResult UpdateBook([FromBody] BookRequest request, int id)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var bookResponse = _bookService.UpdateBook(id, request);

            if (!bookResponse.Success)
            {
                if (!bookResponse.Found)
                {
                    return NotFound(bookResponse.Message);
                }
                return BadRequest(bookResponse.Message);
            }

            return NoContent();
        }

        [HttpDelete("{id}")]
        [SwaggerOperation(Summary = "Deletes book with id")]
        [ApiConventionMethod(typeof(DefaultApiConventions), nameof(DefaultApiConventions.Delete))]
        public IActionResult DeleteBook(int id)
        {
            var bookResponse = _bookService.DeleteBook(id);

            if (!bookResponse.Success)
            {
                if (!bookResponse.Found)
                {
                    return NotFound(bookResponse.Message);
                }
                return BadRequest(bookResponse.Message);
            }
            return Ok();
        }
    }
}