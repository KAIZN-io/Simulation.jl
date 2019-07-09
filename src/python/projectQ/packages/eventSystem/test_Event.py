import unittest
import datetime

from projectQ.packages.eventSystem.Event import Event
from projectQ.packages.values import RFC3339_DATE_FORMAT


class TestEvent(unittest.TestCase):
    def test_constructor(self):
        """
        Tests whether the constructor works as intended
        """
        event = Event({
            'data': 42
        })

        self.assertIs(event.routing_key, 'event')
        self.assertIsInstance(event.emitted_at, datetime.datetime)
        self.assertDictEqual(event.payload, {
            'data': 42
        })

    def test_validate_dict(self):
        """
        Tests whether the validation works as intended
        """

        # It should accept a valid dict
        self.assertTrue(Event.is_valid_dict({
            'routing_key': 'event',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                'data': 42
            }
        }))

        # It should reject an invalid dict
        self.assertFalse(Event.is_valid_dict({
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                'data': 42
            }
        }))
        self.assertFalse(Event.is_valid_dict({
            'routing_key': 'event',
            'payload': {
                'data': 42
            }
        }))
        self.assertFalse(Event.is_valid_dict({
            'routing_key': 'event',
            'emitted_at': '2019-02-24T11:16:16.000',
        }))

    def test_validate_dict_emitted_at_regex(self):
        """
        Tests whether the regex check for the emitted_at attribute is working
        """

        # It should reject an invalid date
        self.assertFalse(Event.is_valid_dict({
            'routing_key': 'event',
            'emitted_at': 'definitely not a utc time string',
            'payload': {
                'data': 42
            }
        }))

    def test_from_dict(self):
        """
        Tests the instance creation from a dict
        """

        event = Event.from_dict({
            'routing_key': 'event',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                'data': 42
            }
        })

        # It should be an instance of Event
        self.assertIsInstance(event, Event)

        # It should have the right routing key
        self.assertIs(event.routing_key, 'event')

        # It should have a datetime object as emitted_at
        self.assertIsInstance(event.emitted_at, datetime.datetime)

        # It should have an unmodified emitted at value
        self.assertEqual(event.emitted_at, datetime.datetime.strptime('2019-02-24T11:16:16.000', RFC3339_DATE_FORMAT))

        # It should have an unmodified payload
        self.assertDictEqual(event.payload, {
            'data': 42
        })

    def test_to_dict(self):
        """
        Tests the dict created by its to_dict method
        """
        event = Event.from_dict({
            'routing_key': 'event',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                'data': 42
            }
        })

        self.assertDictEqual(event.to_dict(), {
            'routing_key': 'event',
            'emitted_at': datetime.datetime.strptime('2019-02-24T11:16:16.000', RFC3339_DATE_FORMAT),
            'payload': {
                'data': 42
            }
        })

    def test_get_routing_key(self):
        """
        Tests whether the correct routign key is set
        """

        # create event
        event = Event({})

        # It should have the routing key as a class var
        self.assertEqual(Event.routing_key, 'event')

        # It should return the correct routing key when calling get_routing_key on the class
        self.assertEqual(Event.get_routing_key(), 'event')

        # It should return the correct routing key when calling get_routing_key on an instance
        self.assertEqual(event.get_routing_key(), 'event')

if __name__ == '__main__':
    unittest.main()

