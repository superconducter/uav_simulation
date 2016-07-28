import os
import unittest

import django
from ui_sim_interface import pass_data

from ui_sim_interface.interface import State, Uav
from ui_sim_interface.models import Agent


class PassingDataTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        #This should match the manage.py entry
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "uavsim.settings")
        django.setup()


    def test_passing_data(self):
        some_state = State()
        observer = pass_data.Observer()
        observer.new_simulation(some_state, "Test_simulation")
        before = Agent.objects.count()
        some_uav = Agent()
        some_uav.velocity = 5
        some_uav.x = 1
        some_uav.y = 2
        some_uav.direction = 5
        some_state.round_number = 1
        some_state.uavs = [some_uav,]
        some_state.fire()
        after = Agent.objects.count()
        self.assertEqual(before + 1, after)


if __name__ == '__main__':
    unittest.main()
