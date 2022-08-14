from api import base, enums
from api.filter import Filter


class GetRealTimeNearStop(base.ApiBase):

    def __init__(self, city: enums.Cities, route_name: str, direction: enums.Directions):
        super().__init__(f'/v2/Bus/RealTimeNearStop/City/{city.value}/{route_name}')
        self.api_filter = (
                (Filter('RouteName/Zh_tw') == route_name) &
                (Filter('Direction') == direction.value) &
                (Filter('A2EventType') == enums.A2EventTypes.ENTER.value)
        ).get_value()

        self._city = city
        self._route_name = route_name
