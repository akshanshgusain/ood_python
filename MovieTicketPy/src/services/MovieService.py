import uuid
from src.exceptions.NotFoundException import NotFoundException
from src.models.Movie import Movie


class MovieService:
    def __init__(self):
        self.movies: dict[str: Movie] = {}

    def get_movies(self, movie_id: str) -> Movie:
        if movie_id in self.movies:
            return self.movies.get(movie_id)
        else:
            raise NotFoundException()

    def create_movie(self, movie_name: str) -> Movie:
        movie_id: str = uuid.uuid4().hex
        movie: Movie = Movie(movie_id, movie_name)
        self.movies[movie_id] = movie
        return movie
