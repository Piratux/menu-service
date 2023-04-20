namespace Infrastructure.BaseModels
{
    public abstract class Response
    {
        public bool Success { get; protected set; }
        public string? Message { get; protected set; } = string.Empty;

        public Response(bool success, string? message)
        {
            Success = success;
            Message = message;
        }
    }
}
