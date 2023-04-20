
FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 80

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["Library/Library.API.csproj", "Library/"]
RUN dotnet restore "Library/Library.API.csproj"
COPY . .
WORKDIR "/src/Library"
RUN dotnet build "Library.API.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "Library.API.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "Library.API.dll"]