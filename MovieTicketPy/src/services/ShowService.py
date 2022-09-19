import uuid
from datetime import datetime
from typing import List

from src.exceptions.NotFoundException import NotFoundException
from src.models.Movie import Movie
from src.models.Screen import Screen
from src.models.Show import Show


class ShowService:
    def __init__(self):
        self.shows: dict[str: Show] = {}

    def get_show(self, show_id: str) -> Show:

        if show_id in self.shows:
            return self.shows.get(show_id)
        else:
            raise NotFoundException()

    # Show Creation
    def create_show(self, movie: Movie,
                    screen: Screen,
                    start_time: datetime,
                    duration_in_seconds: int) -> Show:
        show_id: str = uuid.uuid4().hex
        show: Show = Show(show_id, movie, screen, start_time, duration_in_seconds)
        self.shows[show_id] = show
        return show

    def get_shows_for_screen(self, screen: Screen) -> List[Show]:
        response: List[Show] = []
        for show in self.shows:
            if show.screen == screen:
                response.append(show)
        return response
