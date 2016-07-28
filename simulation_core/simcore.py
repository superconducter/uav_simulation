import simpy
import logging
from UseCaseInterface.World import World
from UseCaseInterface.UseCaseControl import UseCaseControl
from ui_sim_interface.interface import State
from ui_sim_interface.pass_data import Observer
from .json_handler import *

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class SimulationCore:
    def __init__(self, env, data_setting):
        #sets environment settings like size
        self.env = env
        self.axisX = int(str(data_setting["axisX"]).strip("[]"))
        self.axisY = int(str(data_setting["axisY"]).strip("[]"))
        #Variables required to initialize UseCaseControl
        self.velocity = int(str(data_setting["Speed"]).strip("[]"))
        self.sensors = int(str(data_setting["Nr_Sensors"]).strip("[]"))
        self.nr_sensors = int(str(data_setting["Sensors"]).strip("[]"))

        #call UC group class functions
        self.world = World(env)
        self.UseCaseControl = UseCaseControl(self.world, self.nr_sensors, self.sensors, self.velocity)

        #observer for UI group
    def register_sim(self, config):
        self.ui_observer = Observer()
        self.state = State()
        return self.ui_observer.new_simulation(self.state, config)

    def clock(sim, name, tick, wind):
        while True:
            #log current round number
            logging.debug("/// %s %s",name, sim.env.now)
            #lcheck if uavs are in wind zones
            sim.world.wind_machine(sim, wind, sim.env.now)
            #check if uav crashed
            sim.world.crash_check(sim.env.now)
            #request updates from UseCase
            sim.UseCaseControl.calculate_next_step(sim.env.now)
            #fire current state of simulation to UI
            sim.state.round_number = sim.env.now
            sim.state.agents = sim.world.agents
            #fire only events of UAVs that crashed in current round
            event_list = []
            for i, items in enumerate(sim.world.events):
                if sim.env.now == sim.world.events[i].time:
                    event_list.append(sim.world.events[i])
            sim.state.events = event_list
            #fire current state of simulation
            sim.state.fire()

            yield sim.env.timeout(tick)


#config json string and simulation id provided by UI. sim_ui var will be passed back to UI for identification
def main(config, json_data):
    logging.debug("Starting the simulation")
    logging.debug("Simulation Number: %s", config)

    """
    Call json handler in order to get all the parameters of the use cases.
    Return a dictionary of the settings of the use case.
    """
    logging.debug(json_data)
    data_use_cases = []
    data_config = {}
    data_use_cases = json_handler(json_data,data_config)
    #logging.debug("DATA SETTING: %s", data_setting)

    #create simpy environment and initialize simulation
    env = simpy.Environment()
    sim = SimulationCore(env,data_config)

    #sim_id would be an id from UI group (database)
    #passing the config as a parameter when UI is called.
    sim_id = sim.register_sim(config)

    for rec, item in enumerate(data_use_cases):
        sim.UseCaseControl.create_new_use_case(str(data_use_cases[rec]["Type"]).strip("[']"), sim.axisX, sim.axisY,
                                               len(data_use_cases[rec]['UAV']), data_use_cases[rec]['UAV'], sim.env.now)

    # launch usecase and create simpy process and defined number of obstacles
    env.process(SimulationCore.clock(sim, 'ticktock', 1, data_use_cases[0]['Wind']))

    #create world static objects from config
    sim.world.create_static_object(data_use_cases[0]['Building'], type="Building")
    sim.world.create_static_object(data_use_cases[0]['ChargingStation'], type="ChargingStation")
    sim.world.create_static_object(data_use_cases[0]['Wind'], type="Wind")

    #start and define length of simulation
    sim.env.run(until=int(str(data_config["Round"]).strip("[]")))

    logging.debug("End of simulation!")
    return sim_id


if __name__ == '__main__':
    main()