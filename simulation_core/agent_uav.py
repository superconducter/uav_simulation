import numpy as np
import logging
from simulation_core.agent import Agent

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Uav(Agent):
    def __init__(self, posx, posy, velocity=1, status=0, max_load=10, type="uav"):
        #coord. of the agent in axis (x,y)
        self.posx = posx
        self.posy = posy
        self.type = type
        self.status = status
        #max capacity of load of the uav.
        self.max_load = max_load
        #current velocity
        self.initvelocity = velocity
        self.velocity = velocity
        #environment of simpy
        self.id = id(self)
        #Battery levels
        self.cell = 10
        self.maxcell = 100

    def fly(self,E):
        self.status = E
        if (self.status > 2):
            self.status = 1
            #logging.debug("UAV flies")
        else:
            self.status = 0
            #logging.debug("UAV landed")

    # The dirction is outputed by angle
    def direction(self, start, end): #start and end are 2 dimension array
            dist = np.linalg.norm(end - start)
            xdist = np.abs(end[0] - start[0])
            ydist = np.abs(end[1] - start[1])
            if(xdist != 0 and ydist != 0) :
                cos = (dist**2 +xdist**2 -ydist**2)/(2*xdist*dist)
            elif(xdist == 0) :
                cos = 1
            elif(ydist == 0):
                cos = 0
            angle = np.arccos(cos)
            #logging.debug ("cos: ",cos)

            if (start[1] > end[1]):
                if(start[0] > end[0]):
                    angle = -angle - np.pi/2
                else:
                    angle = -angle
            else:
                if(start[0] > end[0]):
                    angle = angle + np.pi/2
                else:
                    angle = angle

            return angle

    def move(self, endx, endy, velocity):
        location = np.zeros(2)
        location[0] = self.posx
        location[1] = self.posy

        end = np.zeros(2)
        end[0] = endx
        end[1] = endy

        culdist = velocity
        angle = self.direction(location, end)

        location[0] = location[0] + np.cos(angle)*culdist
        location[1] = location[1] + np.sin(angle)*culdist

        E = np.linalg.norm(end - location)

        # Error function only works if velocity <= 1
        if (E > 1):
            self.posx = location[0]
            self.posy = location[1]
            self.fly(E)
        else:
            self.posx = endx
            self.posy = endy
            self.fly(E)

        #logging.debug("UAV %s velocity: %s", self.id, self.velocity)
        #logging.debug("UAV %s Angle: %s",self.id, angle)
        #logging.debug("UAV %s new location: %s", self.id, [self.posx, self.posy])

    def next_move(self, x, y, velocity):
        #logging.debug("UAV %s flying to: %s", self.id, [x,y])
        self.move(x, y, velocity)

    def charge(self):
        chrspd = 1
        culcell = 0.
        while(culcell<1):
            self.cell = self.cell + chrspd
            culcell = self.cell/self.maxcell
            logging.debug("Now {0:.2f} percent ".format(round(culcell*100),2))
        self.cell = self.maxcell
        logging.debug("Now 100 percent finished")

    def crash(self, time):
        self.name = "crash"
        self.time = time
        return self

    def turbulence(self, time):
        self.name = "turbulence"
        self.time = time
        return self

    #new function: useEnergy()
    def useEnergy(self, ecost=1): # ecost is a required energy at every round
        if(((self.status==1) | (self.status==3)) & (self.cell != 0)): #In case of flying or in wind area and cell is not empty, a UAV use battery
            self.cell = self.cell - ecost # at every round battery is reduced by ecost 
        print("Battery energy left: ",self.cell )