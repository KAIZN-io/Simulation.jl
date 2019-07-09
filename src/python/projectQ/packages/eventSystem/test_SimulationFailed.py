import unittest
import datetime

from projectQ.packages.eventSystem import SimulationFailed
from projectQ.packages.values import RFC3339_DATE_FORMAT


class TestSimulationFailed(unittest.TestCase):
    def test_constructing_methods(self):
        """
        Tests whether the constructing methods works as intended
        """
        event = SimulationFailed.create( 1, 'Whoopsie...' )

        self.assertDictEqual(event.get_payload(), {
            'id': 1,
            'error': {
                'message': 'Whoopsie...'
            }
        })

        event = SimulationFailed.create( 1, 'Whoopsie...', 'whoopsie, doopsie, doo')

        self.assertDictEqual(event.get_payload(), {
            'id': 1,
            'error': {
                'message': 'Whoopsie...',
                'traceback': 'whoopsie, doopsie, doo'
            }
        })

    def test_validate_dict(self):
        """
        Tests whether the dict validation works as expected
        """

        # It should accept valid dict
        self.assertTrue(SimulationFailed.is_valid_dict({
            'routing_key': 'simulation.failed',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                'id': 1,
                'error': {
                    'message': 'Whoopsie...',
                }
            }
        }))
        self.assertTrue(SimulationFailed.is_valid_dict({
            'routing_key': 'simulation.failed',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                'id': 1,
                'error': {
                    'message': 'Whoopsie...',
                    'traceback': 'whoopsie, doopsie, doo'
                }
            }
        }))

        # It should reject invalid payload
        self.assertFalse(SimulationFailed.is_valid_dict({
            'routing_key': 'simulation.failed',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                'data': 1
            }
        }))

        # It should reject invalid routing key
        self.assertFalse(SimulationFailed.is_valid_dict({
            'routing_key': 'invalid.routing_key',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                'id': 1
            }
        }))

    def test_from_dict(self):
        """
        Tests whether creating an event from dict works as expected
        """

        # create event from dict
        event = SimulationFailed.from_dict({
            'routing_key': 'simulation.failed',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                'id': 1,
                'error': {
                    'message': 'Whoopsie...',
                }
            }
        })

        # It should be an instance of its class
        self.assertIsInstance(event, SimulationFailed)

        # It should have the correct routing key
        self.assertEqual(event.routing_key, 'simulation.failed')

        # It should have the right payload
        self.assertDictEqual(event.payload, {
            'id': 1,
            'error': {
                'message': 'Whoopsie...',
            }
        })

    def test_to_dict(self):
        """
        Tests whether the `to_dict` method is producing a valid dict
        """

        # create event from dict
        event = SimulationFailed({
            'id': 1,
            'error': {
                'message': 'Whoopsie...',
            }
        })

        # It should accept the output of `to_dict` as valid dict
        self.assertFalse(SimulationFailed.is_valid_dict(event.to_dict()))

    def test_get_routing_key(self):
        """
        Tests whether the class returns the correct routing key
        """

        # create an event
        event = SimulationFailed({
            'id': 1,
            'error': {
                'message': 'Whoopsie...',
            }
        })

        # It should have the correct routing key as class value
        self.assertEqual(SimulationFailed.routing_key, 'simulation.failed')

        # It should return the correct routing key from class method
        self.assertEqual(SimulationFailed.get_routing_key(), 'simulation.failed')

        # It should return the correct routing key from class instance
        self.assertEqual(event.get_routing_key(), 'simulation.failed')

if __name__ == '__main__':
    unittest.main()

