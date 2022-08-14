from api import base, enums


class GetRouteInfo(base.ApiBase):

    def __init__(self, city: enums.Cities, route_name: str):
        super().__init__(f'/v2/Bus/Route/City/{city.value}/{route_name}')
        self._city = city
        self._route_name = route_name

    @property
    def data(self) -> dict:
        if len(super().data) > 0:
            return super().data[0]
        return super().data
