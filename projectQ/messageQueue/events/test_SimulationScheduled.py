import unittest
import datetime

from messageQueue.events import SimulationScheduled
from values import RFC3339_DATE_FORMAT


payload = {
    'id': 8,
    'uuid': 'dbc8ff2e-d746-48db-8881-f9664649bf0b',
    'created_at': '2019-02-24T17:06:39.291031',

    'name': 'friendly_spence',
    'image_path': 'combined_models_8.png',
    'started_at': '2019-02-24T17:06:39.402140',
    'finished_at': '2019-02-24T17:08:33.719137',
    'failed_at': None,

    'model_id': 1,
    'model': {},

    'initial_value_set_id': 1,
    'initial_value_set': [],

    'parameter_set_id': 1,
    'parameter_set': [],

    'impulses': [],

    'stimuli': [],

    'type': 'combined_models',

    'signal_type': 2,
    'nacl_impulse': 200,

    'start': 0.0,
    'stop': 80.0,
    'step_size': 0.1,

    'co': 'exstdtc in Sekunden'
}

class TestSimulationScheduled(unittest.TestCase):
    def test_constructor(self):
        """
        Tests that the constructor works as expected
        """
        event = SimulationScheduled(payload)

        self.assertEqual(event.routing_key, 'simulation.scheduled')
        self.assertDictEqual(event.payload, payload)

    def test_validate_dict(self):
        """
        Tests that the constructor works as expected
        """
        self.assertTrue(SimulationScheduled.is_valid_dict({
            'routing_key': 'simulation.scheduled',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                **payload
            }
        }))

    def test_from_dict(self):
        """
        Tests that the constructor works as expected
        """
        event = SimulationScheduled.from_dict({
            'routing_key': 'simulation.scheduled',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                **payload
            }
        })

        self.assertIsInstance(event, SimulationScheduled)
        self.assertEqual(event.routing_key, 'simulation.scheduled')
        self.assertDictEqual(event.payload, payload)

    def test_to_dict(self):
        """
        Tests that the constructor works as expected
        """
        event = SimulationScheduled.from_dict({
            'routing_key': 'simulation.scheduled',
            'emitted_at': '2019-02-24T11:16:16.000',
            'payload': {
                **payload
            }
        })

        self.assertDictEqual(event.to_dict(), {
            'routing_key': 'simulation.scheduled',
            'emitted_at': datetime.datetime.strptime('2019-02-24T11:16:16.000', RFC3339_DATE_FORMAT),
            'payload': {
                **payload
            }
        })

    def test_get_routing_key(self):
        """
        Tests that the constructor works as expected
        """
        event = SimulationScheduled(payload)
        self.assertEqual(SimulationScheduled.routing_key, 'simulation.scheduled')
        self.assertEqual(SimulationScheduled.get_routing_key(), 'simulation.scheduled')
        self.assertEqual(event.get_routing_key(), 'simulation.scheduled')

if __name__ == '__main__':
    unittest.main()

