# BusTracker

## Environment

- Python version >= 3.10

```shell
pip install -r requirements.txt
```

## Usage

1. Prepare client and tracking event.
2. Run the client, client will track every event every 15 seconds.
3. Prepare API id and API key for API calling, 
due to I still not pass the register, 
I will use mock data and won't change during time.

```python
from api.enums import Cities
from client import Client, Event

# Prepare client
client = Client()
# Prepare bus tracker event
event = Event(Cities.TPE, '672', '大鵬新城', '博仁醫院', 3)

# Add event to client
client.add_event(event)
# Start client so it can run continually
client.run()
```

## API

- If you have the API id and API key, put them in `API_ID` and `API_KEY` in `API/base.py`.
- Set `MOCK` to `False` in `API/base.py` and check if API can work.

## Author

- [@allen0099][github]

[github]: https://github.com/allen0099