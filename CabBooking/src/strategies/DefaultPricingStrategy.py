from src.models.Location import Location
from src.strategies.iPricingStrategy import iPricingStrategy


class DefaultPricingStrategy(iPricingStrategy):
    PER_KM_RATE = 10.0

    def find_price(self, from_point: Location, to_point: Location):
        return from_point.distance(to_point) * self.PER_KM_RATE
