from simulation_core.agent_uav import Uav
from simulation_core.agent_obstacle import StaticObject, ChargingStation, Wind
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

'Class for sharing objects between Use Case and Core'
class World:

    'Needs an Simulation environment from the core'
    def __init__(self, env):
        self.uavs = {}
        self.static_objects = []
        self.agents = []
        self.events = []
        self.world = env

    def getUAV(self, uav_id):
        return self.uavs[uav_id]

    def getUAVs(self):
        return self.uavs

    def createUAV(self, posx, posy):
        uav = Uav(posx, posy)
        self.agents.append(uav)
        self.uavs[uav.id] = uav
        logging.debug("Created Agent: %s at %s", uav.type, [uav.posx, uav.posy])
        return uav.id

    def removeUAV(self, uavid):
        del self.uavs[uavid]

    def setnextmove(self, uav_id, x, y, velocity=15):
        if self.uavs[uav_id].status != 2:
            Uav.next_move(self.uavs[uav_id], x, y, velocity)

    #if status = 2 then the drone crashed
    def crash_check(self, time):
        for agent in self.agents:
            if agent.type == "Building":
                for k in self.uavs:
                    if (((agent.posx-agent.lenx)<self.uavs[k].posx)&((agent.posy-agent.leny)<self.uavs[k].posy)&((agent.posx+agent.lenx)>self.uavs[k].posx)&((agent.posy+agent.leny)>self.uavs[k].posy)):
                        if self.uavs[k] not in self.events:
                            self.events.append((Uav.crash(self.uavs[k], time)))
                            self.uavs[k].status = 2
                        #logging.debug("UAV %s CRASHED & BURNED!!!", self.uavs[k].id)

    def create_static_object(self, obstaclelist, type):
        if type == "Building":
            for n in range(len(obstaclelist)):
                self.static_objects.append(StaticObject(obstaclelist[n][0], obstaclelist[n][1],obstaclelist[n][2],obstaclelist[n][3]))
                self.agents.append(StaticObject(obstaclelist[n][0], obstaclelist[n][1],obstaclelist[n][2],obstaclelist[n][3]))
                logging.debug("Created Agent: %s at %s", type, [obstaclelist[n][0], obstaclelist[n][1],obstaclelist[n][2],obstaclelist[n][3]])
        elif type == "ChargingStation":
            for n in range(len(obstaclelist)):
                self.static_objects.append(ChargingStation(obstaclelist[n][0], obstaclelist[n][1],obstaclelist[n][2],obstaclelist[n][3]))
                self.agents.append(ChargingStation(obstaclelist[n][0], obstaclelist[n][1],obstaclelist[n][2],obstaclelist[n][3]))
                logging.debug("Created Agent: %s at %s", type, [obstaclelist[n][0], obstaclelist[n][1],obstaclelist[n][2],obstaclelist[n][3]])
        elif type == "Wind":
            for n in range(len(obstaclelist)):
                self.static_objects.append(Wind(obstaclelist[n][0], obstaclelist[n][1],obstaclelist[n][2],obstaclelist[n][3]))
                self.agents.append(Wind(obstaclelist[n][0], obstaclelist[n][1],obstaclelist[n][2],obstaclelist[n][3]))
                logging.debug("Created Agent: %s at %s", type, [obstaclelist[n][0], obstaclelist[n][1],obstaclelist[n][2],obstaclelist[n][3]])

    def get_static_objects(self):
        return self.static_objects

    #loop through winds and check if uavs are inside
    def wind_machine(self, sim, wind, time):
        for n in range(len(wind)):
                sim.wind = Wind(wind[n][0], wind[n][1], wind[n][2], wind[n][3])
                sim.wind.update_sim(sim)
                sim.wind.make_wind()
        for k in self.uavs:
            if self.uavs[k] not in self.events:
                if self.uavs[k].status == 3:
                    self.events.append((Uav.turbulence(self.uavs[k], time)))