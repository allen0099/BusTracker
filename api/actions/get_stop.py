from api import base


class GetStop(base.ApiBase):
    def __init__(self, city: str):
        super().__init__(f'/v2/Bus/Stop/City/{city}')
