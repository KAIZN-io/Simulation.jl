import unittest
import datetime

from eventSystem import SimulationStarted
from values import RFC3339_DATE_FORMAT


class TestSimulationStarted(unittest.TestCase):
    def test_constructing_methods(self):
        """
        Tests whether the constructing methods works as intended
        """
        event = SimulationStarted.create( 1 )

        self.assertDictEqual(event.payload, {
            'id': 1
        })

    def test_validate_dict(self):
        """
        Tests whether the dict validation works as expected
        """

        # It should accept valid dict
        self.assertTrue(SimulationStarted.is_valid_dict({
            'routing_key': 'simulation.started',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                'id': 1
            }
        }))

        # It should reject invalid payload
        self.assertFalse(SimulationStarted.is_valid_dict({
            'routing_key': 'simulation.started',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                'data': 1
            }
        }))

        # It should reject invalid routing key
        self.assertFalse(SimulationStarted.is_valid_dict({
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
        event = SimulationStarted.from_dict({
            'routing_key': 'simulation.started',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                'id': 1
            }
        })

        # It should be an instance of its class
        self.assertIsInstance(event, SimulationStarted)

        # It should have the correct routing key
        self.assertEqual(event.routing_key, 'simulation.started')

        # It should have the right payload
        self.assertDictEqual(event.payload, {
            'id': 1
        })

    def test_to_dict(self):
        """
        Tests whether the `to_dict` method is producing a valid dict
        """

        # create event from dict
        event = SimulationStarted({
            'id': 1
        })

        # It should accept the output of `to_dict` as valid dict
        self.assertFalse(SimulationStarted.is_valid_dict(event.to_dict()))

    def test_get_routing_key(self):
        """
        Tests whether the class returns the correct routing key
        """

        # create an event
        event = SimulationStarted({
            'id': 1
        })

        # It should have the correct routing key as class value
        self.assertEqual(SimulationStarted.routing_key, 'simulation.started')

        # It should return the correct routing key from class method
        self.assertEqual(SimulationStarted.get_routing_key(), 'simulation.started')

        # It should return the correct routing key from class instance
        self.assertEqual(event.get_routing_key(), 'simulation.started')

if __name__ == '__main__':
    unittest.main()

