import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from requests import request, Response, post

from api import enums

BASE_DIR = Path(__file__).resolve().parent.parent


class ApiBase:
    BASE_URL: str = 'https://tdx.transportdata.tw/api/basic/'

    ACCESS_TOKEN: Optional[str] = None
    EXPIRE_DATE: Optional[datetime] = None

    APP_ID: str = os.getenv('APP_ID')
    APP_KEY: str = os.getenv('APP_KEY')

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
            headers=self.get_data_header()
        )

    @property
    def data(self):
        req = self.get()

        # if self.MOCK:
        #     # Mock data from API route, file name is resource name
        #     test_file = self.api_route.split('/')[3]
        #
        #     with open(f"{BASE_DIR}/json/{test_file}.json", encoding="UTF-8") as f:
        #         return json.load(f)

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

    def _refresh_token(self) -> None:
        if not self.EXPIRE_DATE:
            # Set expire date to 1 hour before now
            self.EXPIRE_DATE = datetime.now() + timedelta(hours=-1)

        if self.EXPIRE_DATE < datetime.now():
            # Modified from
            # https://github.com/tdxmotc/SampleCode/blob/master/Python3/auth_TDX.py
            auth_url: str = 'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token'
            r: Response = post(auth_url, {
                'content-type': 'application/x-www-form-urlencoded',
                'grant_type': 'client_credentials',
                'client_id': self.APP_ID,
                'client_secret': self.APP_KEY
            })

            if not r.ok:
                raise Exception(r.text)

            auth_data: dict = r.json()

            self.ACCESS_TOKEN = auth_data.get('access_token')
            self.EXPIRE_DATE = datetime.now() + timedelta(seconds=auth_data.get('expires_in'))

    def get_data_header(self):
        self._refresh_token()

        return {
            'authorization': 'Bearer ' + self.ACCESS_TOKEN
        }
