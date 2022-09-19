from datetime import datetime
from typing import List

from src.models.Movie import Movie
from src.models.Screen import Screen
from src.models.Seat import Seat
from src.models.Show import Show
from src.services.MovieService import MovieService
from src.services.SeatAvailabilityService import SeatAvailabilityService
from src.services.ShowService import ShowService
from src.services.TheaterService import TheaterService


class ShowController:
    def __init__(self, seat_availability_service: SeatAvailabilityService,
                 show_service: ShowService, theater_service: TheaterService
                 , movie_service: MovieService):
        self.seat_availability_service: SeatAvailabilityService = seat_availability_service
        self.show_service: ShowService = show_service
        self.theater_service: TheaterService = theater_service
        self.movie_service: MovieService = movie_service

    def create_show(self, movie_id: str, screen_id: str, start_time: datetime,
                    duration_in_seconds: int) -> str:
        screen: Screen = self.theater_service.get_screen(screen_id)
        movie: Movie = self.movie_service.get_movies(movie_id)
        return self.show_service.create_show(movie, screen, start_time, duration_in_seconds).id

    def get_available_seats(self, show_id: str) -> List[str]:
        show: Show = self.show_service.get_show(show_id)
        available_seats: List[Seat] = self.seat_availability_service.get_available_seats(show)
        available_seats_ = []
        for seat in available_seats:
            available_seats_.append(seat.id)
        return available_seats_
