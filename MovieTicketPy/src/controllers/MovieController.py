from src.services.MovieService import MovieService


class MovieController:

    def __init__(self, movie_service: MovieService):
        self.movie_service: MovieService = movie_service

    def create_movie(self, movie_name: str) -> str:
        return self.movie_service.create_movie(movie_name).id
