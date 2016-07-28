import os
import django
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

print(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ui.uavsim.settings")
django.setup()

from django.db import transaction
from ui_sim_interface.models import Agent, Round, Simulation,Event

possible_status = {
    0: "land",
    1: "fly",
    2: "crash",
    3: "wind"
}

def next_round(state, simulation):
    # Get the relevant settings module from manage.py
    print("Round number {} is being transmitted to UI...".format(state.round_number))
    with transaction.atomic():
        try:
            round = Round()
            round.round_number = state.round_number
            round.simulation = simulation
            round.save()
            for agent in state.agents:
                db_agent = Agent()
                db_agent.round = Round.objects.get(round_number=state.round_number, simulation=simulation)
                db_agent.lat = agent.posx
                db_agent.lng = agent.posy
                db_agent.identifier = agent.id
                db_agent.status = possible_status.get(agent.status)
                db_agent.type = agent.type
                db_agent.save()
            events = None
            try:
                events = state.events
            except AttributeError as e:
                events = []
                print("No events supplied")

            for event in events:
                db_event = Event()
                db_event.round = round
                db_event.lat = event.posx
                db_event.lng = event.posy
                db_event.name = event.name
                db_event.save()

        except AttributeError as e:
            logging.debug("There was an error parsing the state. No changes were saved")
            raise
    logging.debug("Successfully saved %s events this round", len(state.events))
    logging.debug("Successfully saved %s agents this round", len(state.agents))

def complete_simulation(pk=None):
    if not pk:
        raise AttributeError("No simulation key provided")
    simulation = Simulation.objects.get(pk=int(pk))
    simulation.completed = True
    simulation.save()

class Observer(object):
    def notify(self, observable):
        next_round(observable, self.simulation)
    def new_simulation(self, observable, sim_id, force=False):
        try:
            self.simulation = Simulation.objects.get(pk=int(sim_id))
        except Simulation.DoesNotExist as e:
            if force:
                self.simulation = Simulation()
                self.simulation.settings = "{}"
                self.simulation.name = "Unconfigured simulation"
                self.simulation.save()
        observable.subscribe(self)



if __name__ == "__main__":
    print("You should not call this script directly!")


