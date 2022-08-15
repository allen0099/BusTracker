# BusTracker

## Prepare environment

- Python version >= 3.10

```shell
# In virtual environment
pip install -r requirements.txt

# Prepare API ID and API Key here
cp .env.example .env
```

## Example

1. Prepare client and tracking event.
2. Run the client, client will track every event every 15 seconds.

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

## Future Work

- [X] Use real API to fetch data.
- [ ] Rewrite API call methods.
- [ ] Allow to add event after client start.
- [ ] Allow cancel event after client start.
- [ ] Make sure events are always unique, override `__new__` and `__init__` method?

## Author

- [@allen0099][github]

[github]: https://github.com/allen0099