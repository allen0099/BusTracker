import base64
import hmac
import json
from datetime import datetime
from hashlib import sha1
from pathlib import Path
from time import mktime
from typing import Optional
from wsgiref.handlers import format_date_time

from requests import request, Response

from api import enums

BASE_DIR = Path(__file__).resolve().parent.parent


class ApiBase:
    BASE_URL: str = 'https://ptx.transportdata.tw/MOTC'
    APP_ID: str = ''
    APP_KEY: str = ''
    MOCK: bool = True

    def __init__(self, route: str = None):
        self.api_route: Optional[str] = route
        self.api_select: Optional[str] = None
        self.api_filter: Optional[str] = None
        self.api_orderby: Optional[str] = None
        self.api_top: Optional[int] = None
        self.api_skip: Optional[int] = None
        self.api_spatialFilter: Optional[str] = None

        self._city: Optional[enums.Cities] = None
        self._route_name: Optional[str] = None

    def get(self) -> Response:
        if not self.api_route:
            raise Exception('API route not defined')

        return request(
            'GET', f'{self.BASE_URL}{self.api_route}',
            params=self.params,
            headers=self.auth_header
        )

    @property
    def data(self):
        req = self.get()

        if self.MOCK:
            # Mock data from API route, file name is resource name
            test_file = self.api_route.split('/')[3]

            with open(f"{BASE_DIR}/json/{test_file}.json", encoding="UTF-8") as f:
                return json.load(f)

        if req.ok:
            return req.json()

        raise Exception(req.text)

    @property
    def city(self):
        if self._city:
            return self._city

    @property
    def route_name(self):
        if self._route_name:
            return self._route_name

    @property
    def params(self) -> dict[str, str]:
        return_data: dict[str, str] = {
            '$format': 'JSON'
        }

        for _ in ['select', 'filter', 'orderby', 'top', 'skip', 'spatialFilter']:
            if getattr(self, f'api_{_}'):
                return_data[f'${_}'] = getattr(self, f'api_{_}')

        return return_data

    @property
    def auth_header(self) -> dict[str, str]:
        # https://github.com/ptxmotc/Sample-code/blob/master/Python3/auth.py
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.APP_KEY.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.APP_ID + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept-Encoding': 'gzip'
        }
