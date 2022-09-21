from src.models.Location import Location


class Cab:
    def __init__(self, id: str, driver_name: str):
        self.id = id
        self.driver_name: str = driver_name
        self.is_available: bool = True
        self.current_trip_id: str = "-90"
        self.current_location: Location = Location(0, 0)
