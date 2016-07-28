#!/usr/bin/python
import logging
from simulation_core.agent import Agent

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class StaticObject(Agent):
    def __init__(self, posx, posy, lenx, leny, status=0, type="Building"):
        self.posx = posx
        self.posy = posy
        self.lenx = lenx
        self.leny = leny
        self.status = status
        self.type = type
        self.id = id(self)


class ChargingStation(StaticObject):
    def __init__(self, posx, posy, lenx, leny,status=0, limit=10):
        super().__init__(posx, posy, lenx, leny, type="ChargingStation")
        self.status = status
        self.limit = limit
        self.curNumUav = 0
        self.Uavlist = []

    # station is a class of chargingstation. Self is Uav class
    def chargepermit(self, uav, station):

        if station.limit==station.curNumUav:
            logging.debug("Sorry we are full")
        else:
            logging.debug("Welcome!")
            station.curNumUav += 1
            station.Uavlist.append(uav.id)
            uav.charge()


class Wind(StaticObject):
    def __init__(self, posx, posy, lenx, leny, status=0, windspeed=0.5):
        super().__init__(posx, posy, lenx, leny, type="wind")
        self.status = status
        self.windspeed = windspeed

    def update_sim(self, sim):
        self.sim = sim

    def weather_report(self):
        #check for each UAV if it is in a wind area
        for k in self.sim.world.uavs:
            if(((self.posx-self.lenx)<self.sim.world.uavs[k].posx) & ((self.posy-self.leny)<self.sim.world.uavs[k].posy) &((self.posx+self.lenx)>self.sim.world.uavs[k].posx) & ((self.posy+self.leny)>self.sim.world.uavs[k].posy)):
               #status 3 indicates that a UAV is in a wind area
               self.sim.world.uavs[k].status = 3

    def make_wind(self):# uav is a Uav class
        self.weather_report()
        for k in self.sim.world.uavs:
            #check if a UAV is crashed
            if self.sim.world.uavs[k].status != 2:
                #status 3 means a UAV is in a wind area
                if((self.sim.world.uavs[k].status == 3) & (self.sim.world.uavs[k].velocity == self.sim.world.uavs[k].initvelocity) ):
                    self.sim.world.uavs[k].velocity = self.sim.world.uavs[k].velocity*self.windspeed
                else:
                    #if it is not in a windy area set UAV to its initial velocity and status fly
                    self.sim.world.uavs[k].velocity = self.sim.world.uavs[k].initvelocity
                    self.sim.world.uavs[k].status = 1
