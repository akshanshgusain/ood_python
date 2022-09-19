from dataclasses import dataclass
from datetime import datetime

from src.models.Movie import Movie
from src.models.Screen import Screen


@dataclass(frozen=True, eq=True)
class Show:
    id: str
    movie: Movie
    screen: Screen
    start_time: datetime
    duration_in_seconds: int

    def __hash__(self):
        return id(self)
