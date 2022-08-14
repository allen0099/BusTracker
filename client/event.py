from typing import Optional, Any

from api.actions import GetRouteInfo, GetRouteStops, GetRealTimeNearStop
from api.enums import Cities, Directions


class Event:
    def __init__(self, city: Cities, route_name: str, toward: str, destination: str, notify_before: int = 3):
        self.city: Cities = city
        """城市名"""
        self.route_name: str = route_name
        """路線名"""
        self.toward: str = toward
        """前往方向"""
        self.destination: str = destination
        """目的站名"""
        self.notify_before: int = notify_before
        """幾站前通知"""

        self._route_info: Optional[dict] = None
        self._direction: Optional[Directions] = None
        self._route_stops: Optional[GetRouteStops] = None
        self._destination_stop: Optional[dict[str, Any]] = None
        self._notify_stop: Optional[dict[str, Any]] = None

        self.is_notified: bool = False

    @property
    def route_info(self) -> dict:
        """路線資訊"""
        if self._route_info:
            return self._route_info

        data: dict = GetRouteInfo(self.city, self.route_name).data
        self._route_info = data
        return data

    @property
    def direction(self) -> Directions:
        """前往方向"""
        if self._direction:
            return self._direction

        direction: Directions = Directions.UNKNOWN

        for target in ["Departure", "Destination"]:
            if direction != Directions.UNKNOWN:
                break

            for language in ["Zh", "En"]:
                if self.route_info.get(f"{target}StopName{language}") == self.toward:

                    match (target):
                        case "Departure":
                            direction = Directions.BACK

                        case "Destination":
                            direction = Directions.GO

                        case _:
                            direction = Directions.UNKNOWN

                    break
        self._direction = direction
        return direction

    @property
    def route_stops(self) -> GetRouteStops:
        """路線站點"""
        if self._route_stops:
            return self._route_stops

        self._route_stops = GetRouteStops(self.city, self.route_name, direction=self.direction)
        return self._route_stops

    @property
    def stops(self) -> list[dict[str, Any]]:
        return self.route_stops.data

    @property
    def destination_stop(self) -> dict[str, Any]:
        """目的站點資訊"""
        if self._destination_stop:
            return self._destination_stop

        self._destination_stop = self.route_stops.find_stop(self.destination)
        return self._destination_stop

    @property
    def notify_stop(self) -> dict[str, Any]:
        """通知站點資訊"""
        if self._notify_stop:
            return self._notify_stop
        _before: int = self.destination_stop.get('StopSequence') - self.notify_before

        if _before < 0:
            raise ValueError("Notify stop is out of range")

        self._notify_stop = self.route_stops.get_stop_by_sequence(_before)
        return self._notify_stop

    def get_realtime_near_stop(self) -> list[dict[str, Any]]:
        data: list[dict[str, Any]] = GetRealTimeNearStop(self.city, self.route_name, self.direction).data
        return data

    def is_bus_arrived_notify_stop(self) -> bool:
        """是否已到達通知站點"""
        for bus in self.get_realtime_near_stop():
            if bus.get('StopUID') == self.notify_stop.get('StopUID'):
                return True
        return False

    def notify(self):
        if self.is_notified:
            return
        print(f"{self.route_name} is approaching to {self.destination}!")
        self.is_notified = True

    def check_bus_status(self):
        print(f"Checking {self.route_name} status...")
        if self.is_bus_arrived_notify_stop():
            self.notify()
