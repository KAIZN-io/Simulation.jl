import unittest
import datetime

from projectQ.packages.db import Ex

class TestEvent(unittest.TestCase):
    def test_ex_dict_validation(self):
        """
        Tests whether the constructor works as intended
        """
        ex_dict = {
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
            'initial_value_set': [
                {
                    'comment': 'original/hog_model',
                    'orres': '0.0000424318676149895',
                    'orresu': 'mM',
                    'precedence': 1,
                    'testcd': 'Pbs2'
                }
            ],

            'parameter_set_id': 1,
            'parameter_set': [
                {
                    'comment': '',
                    'orres': '303.15',
                    'orresu': 'K',
                    'precedence': 1,
                    'testcd': 'T'
                }
            ],

            'impulses': [
                {
                    'start': 1.0,
                    'stop': 13.0,
                    'substance': 'Glucose'
                }
            ],

            'stimuli': [
                {
                    'active': True,
                    'amount': 100.0,
                    'substance': 'KCl',
                    'targets': ['K_out', 'Cl_out'],
                    'timings': [30, 60, 100],
                    'unit': 'mM'
                }
            ],

            'type': 'combined_models',

            'signal_type': 2,
            'nacl_impulse': 200,

            'start': 0.0,
            'stop': 80.0,
            'step_size': 0.1,

            'co': 'exstdtc in Sekunden'
        }

        self.assertTrue(Ex.get_dict_schema().validate(ex_dict))

        ex_dict = {
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

        self.assertTrue(Ex.get_dict_schema().validate(ex_dict))

if __name__ == '__main__':
    unittest.main()

