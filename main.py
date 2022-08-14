from api.enums import Cities
from client import Client, Event

if __name__ == '__main__':
    client = Client()
    client.add_event(Event(Cities.TPE, '672', '大鵬新城', '博仁醫院', 3))
    client.run()
