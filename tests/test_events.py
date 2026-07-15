import unittest

from engine.events import Event, EventBus


class TestEvent(Event):
    pass


class OtherEvent(Event):
    pass


class EventBusTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.bus = EventBus()
        self.events: list[Event] = []

    def test_subscribe_and_publish(self) -> None:
        def listener(event: Event) -> None:
            self.events.append(event)

        self.bus.subscribe(TestEvent, listener)
        event = TestEvent()
        self.bus.publish(event)

        self.assertEqual(self.events, [event])

    def test_multiple_listeners(self) -> None:
        calls: list[str] = []

        def first(event: Event) -> None:
            calls.append("first")

        def second(event: Event) -> None:
            calls.append("second")

        self.bus.subscribe(TestEvent, first)
        self.bus.subscribe(TestEvent, second)
        self.bus.publish(TestEvent())

        self.assertEqual(calls, ["first", "second"])

    def test_unsubscribe_removes_listener(self) -> None:
        calls: list[str] = []

        def listener(event: Event) -> None:
            calls.append("called")

        self.bus.subscribe(TestEvent, listener)
        self.bus.unsubscribe(TestEvent, listener)
        self.bus.publish(TestEvent())

        self.assertEqual(calls, [])

    def test_publish_without_listeners_does_not_raise(self) -> None:
        try:
            self.bus.publish(OtherEvent())
        except Exception as exc:
            self.fail(f"publish raised an exception: {exc}")

    def test_listener_for_one_event_type_does_not_receive_other_type(self) -> None:
        calls: list[str] = []

        def listener(event: Event) -> None:
            calls.append("called")

        self.bus.subscribe(TestEvent, listener)
        self.bus.publish(OtherEvent())

        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
