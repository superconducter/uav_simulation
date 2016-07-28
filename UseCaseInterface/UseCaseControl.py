from UseCaseInterface.Advertisment import Advertisment
from UseCaseInterface.Delivery import Delivery
from UseCaseInterface.Defense import Defense
from UseCaseInterface.Statistics import UseCaseStatistic
import logging

'Class to create Use Cases and initiate their actions each round'
class UseCaseControl:

    'To create an Use Case Control give: a World object, Sensorrange, Max Speed of UAVs, Number of sensors'
    def __init__(self, env, sensor, speed, nr_sensor):
        self.sensor_range = sensor
        self.uav_speed = speed
        self.sensor_number = nr_sensor
        self.world = env
        self.usecases = {}
        self.usecase_id = 0
        self.stats = UseCaseStatistic()

    'Call every round to calculate Use Case and UAVs actions'
    def calculate_next_step(self, timestamp):

        logging.debug(timestamp)
        self.stats.return_stats()
        #logging.debug("in")
        for uc_id, usecase in self.usecases.items():
            usecase.calculate_action(timestamp)
        #logging.debug("out")

    '''
    To create an Use Case give: type, x- and y-Coordinate, Number of UAVs and current round number
    Types are: Advertisement, Delivery, Defense
    '''
    def create_new_use_case(self, init_type, x, y, n_uavs, list_coord_uav, timestamp):

        if n_uavs <= 0:
            print("Please put in a number of UAVs > 0")
            return

        if init_type == "Advertisement": usecase = Advertisment(x, y, self.usecase_id, timestamp, self.world, self)
        elif init_type == "Crowd":
            logging.debug("Crowd Managment not implemented in current version!")
            return
        elif init_type == "Delivery": usecase = Delivery(x, y, self.usecase_id, n_uavs, list_coord_uav, timestamp, self.world, self)
        elif init_type == "Defense": usecase = Defense(x, y, self.usecase_id, n_uavs, timestamp, self.world, self)
        else:
            logging.debug("Not a valid Use Case type. The types are Advertisement, Delivery and Defense.")
            return

        self.usecases[self.usecase_id] = usecase
        self.usecase_id += 1

    'Function to check if there are buildings at certain points to make sure no job is created inside'
    def check_space(self, poslist):
        for pos in poslist:
            x = pos[0]
            y = pos[1]
            for agent in self.world.agents:
                if agent.type == "Building":
                    if (((agent.posx - agent.lenx) < x) & ((agent.posy - agent.leny) < y)
                            & ((agent.posx + agent.lenx) > x) & ((agent.posy + agent.leny) > y)):
                        return True
        return False

    'Events that can happen: Job created, done, failed and timed out. Adding them to statistics.'
    def event(self, case, type):
        if case == "Advert":
            if type == "Timed":
                self.stats.job_timed("Advert")
            elif type == "New":
                self.stats.job_created("Advert")
            elif type == "Done":
                self.stats.job_done("Advert")
            elif type == "Failed":
                self.stats.job_failed("Advert")
            else:
                logging.debug("Use Case Control Event Error Advert Type: " + str(type))

        elif case == "Delivery":
            if type == "Done":
                self.stats.job_done("Delivery")
            elif type == "Timed":
                self.stats.job_timed("Delivery")
            elif type == "New":
                self.stats.job_created("Delivery")
            elif type == "Failed":
                self.stats.job_failed("Delivery")
            else:
                logging.debug("Use Case Control Event Error Delivery Type: " + str(type))

        elif case == "Defense":
            if type == "Done":
                self.stats.job_done("Defense")
            elif type == "New":
                self.stats.job_created("Defense")
            elif type == "Failed":
                self.stats.job_failed("Defense")
            else:
                logging.debug("Use Case Control Event Error Defense Type: " + str(type))

        else:
            logging.debug("Use Case Control Event Error Case: " + str(case))

    'Giving events to the world to pass to UI'
    def add_event(self, time, posx, posy, name):
        self.world.events.append(WorldEvent(time, posx, posy, name))


class WorldEvent:

    def __init__(self, time, posx, posy, name):
        self.time = time
        self.posx = posx
        self.posy = posy
        self.name = name