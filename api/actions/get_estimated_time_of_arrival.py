from api import base, enums
from api.filter import Filter

"""
EstimateTime (second) [
當 StopStatus 値為 2 ~ 4 或 PlateNumb 値為 -1 時，EstimateTime 値為 null; 
當 StopStatus 値為 1 時，EstimateTime 値多數為 null，僅部分路線因有固定發車時間，故 EstimateTime 有値; 
當 StopStatus 値為 0 時，EstimateTime 有値。]
"""
"""
StopStatus : [0:'正常',1:'尚未發車',2:'交管不停靠',3:'末班車已過',4:'今日未營運']
"""


class GetEstimatedTimeOfArrival(base.ApiBase):

    def __init__(self, city: enums.Cities, route_name: str):
        super().__init__(f'/v2/Bus/EstimatedTimeOfArrival/City/{city.value}/{route_name}')
        self.api_filter = (Filter('RouteName/Zh_tw') == route_name).get_value()

        self._city = city
        self._route_name = route_name
