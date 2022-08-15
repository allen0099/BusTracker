from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=str(Path(__file__).parent / ".env"), verbose=True)

if __name__ == '__main__':
    from api.enums import Cities
    from client import Client, Event

    client = Client()
    client.add_event(Event(Cities.TPE, '672', '大鵬新城', '博仁醫院', 3))
    client.run()
