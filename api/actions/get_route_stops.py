from api import base
from api.enums import Cities, Directions
from api.filter import Filter


class GetRouteStops(base.ApiBase):

    def __init__(self, city: Cities, route_name: str, display: bool = False,
                 direction: Directions = Directions.UNKNOWN):
        endpoint: str = f'/v2/Bus/StopOfRoute/City/{city.value}/{route_name}'

        if display:
            endpoint = f'/v2/Bus/DisplayStopOfRoute/City/{city.value}/{route_name}'

        super().__init__(endpoint)
        self.api_filter = (Filter('RouteName/Zh_tw') == route_name).get_value()
        self.direction = direction

        self._city = city
        self._route_name = route_name

    def find_stop(self, stop_name: str) -> dict:
        for stop in self.data:
            _name_label: dict = stop.get('StopName')
            if _name_label:
                for language in ['Zh_tw', 'En']:
                    if _name_label.get(language) == stop_name:
                        return stop

        raise ValueError(f"Stop {stop_name} not found in {self._city} {self._route_name}")

    def get_stop_by_sequence(self, seq: int) -> dict:
        for stop in self.data:
            if stop.get('StopSequence') == seq:
                return stop

        raise ValueError(f"Stop id {seq} not found in {self._city} {self._route_name}")

    @property
    def data(self) -> list[dict]:
        original_data: list[dict] = super().data

        if self.direction != Directions.UNKNOWN:
            for _ in original_data:
                if _['Direction'] == self.direction.value:
                    return _.get('Stops')

        raise Exception(f'{self._city.value} {self._route_name} {self.direction} not found')
