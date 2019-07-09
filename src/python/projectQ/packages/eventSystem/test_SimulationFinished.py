import unittest
import datetime

from projectQ.packages.eventSystem import SimulationFinished
from projectQ.packages.values import RFC3339_DATE_FORMAT


class TestSimulationFinished(unittest.TestCase):
    def test_validate_dict(self):
        """
        Tests whether the dict validation works as expected
        """

        # It should accept valid dict
        self.assertTrue(SimulationFinished.is_valid_dict({
            'routing_key': 'simulation.finished',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                'id': 1,
                'extrt': 'KCl',
                'exdose': 100,
                'exstdtc_array': [30, 60, 100],
                'image_path': 'ion_9.png',
                'pds': [{}]
            }
        }))

    def test_from_dict(self):
        """
        Tests whether creating an event from dict works as expected
        """

        # create event from dict
        event = SimulationFinished.from_dict({
            'routing_key': 'simulation.finished',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                'id': 1,
                'extrt': 'KCl',
                'exdose': 100,
                'exstdtc_array': [30, 60, 100],
                'image_path': 'ion_9.png',
                'pds': [{}]
            }
        })

        # It should be an instance of its class
        self.assertIsInstance(event, SimulationFinished)

        # It should have the correct routing key
        self.assertEqual(event.routing_key, 'simulation.finished')

        # It should have the right payload
        self.assertDictEqual(event.payload, {
            'id': 1,
            'extrt': 'KCl',
            'exdose': 100,
            'exstdtc_array': [30, 60, 100],
            'image_path': 'ion_9.png',
            'pds': [{}]
        })

    def test_get_routing_key(self):
        """
        Tests whether the class returns the correct routing key
        """

        # create an event
        event = SimulationFinished({
            'id': 1,
            'extrt': 'KCl',
            'exdose': 100,
            'exstdtc_array': [30, 60, 100],
            'image_path': 'ion_9.png',
            'pds': [{}]
        })

        # It should have the correct routing key as class value
        self.assertEqual(SimulationFinished.routing_key, 'simulation.finished')

        # It should return the correct routing key from class method
        self.assertEqual(SimulationFinished.get_routing_key(), 'simulation.finished')

        # It should return the correct routing key from class instance
        self.assertEqual(event.get_routing_key(), 'simulation.finished')

if __name__ == '__main__':
    unittest.main()

