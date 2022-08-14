import asyncio
from signal import signal, SIGINT, SIGTERM, SIGABRT

from client.event import Event


class Client:
    CHECK_TIME: int = 15

    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.events: list[Event] = []

    def run(self):
        run = self.loop.run_until_complete
        run(self.start())
        run(self.stop())

    def add_event(self, tracking_event: Event):
        self.events.append(tracking_event)

    async def routine_check(self):
        print("Checking...")

        for event in self.events:
            # Check bus status here, can call event methods directly
            event.check_bus_status()

            if event.is_notified:
                print(f"{event.route_name} is notified, remove from events...")
                self.events.remove(event)

        await asyncio.sleep(self.CHECK_TIME)

    async def start(self):
        print("Starting...")
        print("Press Ctrl+C to stop...")
        print(f"Added {len(self.events)} events...")

        task = None

        def cancel_task(_, __):
            print("SIGNAL stop received, exiting...")
            task.cancel()

        for signum in (SIGINT, SIGTERM, SIGABRT):
            signal(signum, cancel_task)

        while True:
            task = asyncio.create_task(self.routine_check())

            try:
                await task
            except asyncio.CancelledError:
                break

    async def stop(self):
        print("Stopping...")

        self.events.clear()
