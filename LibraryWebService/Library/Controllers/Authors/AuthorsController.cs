using Infrastructure.Domains.Authors.Models;
using Infrastructure.Domains.Authors.Services;
using Microsoft.AspNetCore.Mvc;
using Swashbuckle.AspNetCore.Annotations;

namespace Library.API.Controllers.Authors
{
    [ApiController]
    [Route("api/[controller]")]
    public class AuthorsController : ControllerBase
    {
        private readonly IAuthorService _authorService;
        public AuthorsController(IAuthorService authorService)
        {
            _authorService = authorService;
        }

        [HttpGet]
        [SwaggerOperation(Summary = "Returns all authors")]
        [ApiConventionMethod(typeof(DefaultApiConventions), nameof(DefaultApiConventions.Get))]
        public IActionResult GetAllAuthors()
        {
            return Ok(_authorService.GetAllAuthors());
        }

        [HttpGet("{id}")]
        [SwaggerOperation(Summary = "Returns author by id")]
        [ApiConventionMethod(typeof(DefaultApiConventions), nameof(DefaultApiConventions.Get))]
        public IActionResult GetAuthor(int id)
        {
            var response = _authorService.GetAuthor(id);
            if (!response.Success)
            {
                return NotFound(response.Message);
            }
            return Ok(response.Author);
        }

        [HttpPost]
        [SwaggerOperation(Summary = "Creates new author")]
        [ApiConventionMethod(typeof(DefaultApiConventions), nameof(DefaultApiConventions.Post))]
        public IActionResult CreateAuthor([FromBody] AuthorRequest request)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }
            var response = _authorService.CreateAuthor(request);
            if(!response.Success)
            {
                return BadRequest(response.Message);
            }
            return CreatedAtAction(nameof(GetAuthor), new { id = response.Author?.Id }, response.Author);
        }

        [HttpPut("{id}")]
        [SwaggerOperation(Summary = "Updates author by id")]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        public IActionResult UpdateAuthor(int id, [FromBody] AuthorRequest request)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }
            var response = _authorService.UpdateAuthor(id, request);
            if(!response.Success)
            {
                if (!response.Found)
                {
                    return NotFound(response.Message);
                }
                return BadRequest(response.Message);
            }
            return Ok(response.Author);
        }

        [HttpDelete("{id}")]
        [SwaggerOperation(Summary = "Deletes author with id")]
        [ApiConventionMethod(typeof(DefaultApiConventions), nameof(DefaultApiConventions.Delete))]
        public IActionResult DeleteAuthor(int id)
        {
            var response = _authorService.DeleteAuthor(id);
            if(!response.Success)
            {
                if (!response.Found)
                {
                    return NotFound(response.Message);
                }
                return BadRequest(response.Message);
            }
            return Ok();
        }
    }
}
