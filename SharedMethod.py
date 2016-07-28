import sys

from numpy.random import *

from simulation_core.agent import *


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
    print ("cos: ",cos)
        
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
  

def move(self, endx, endy):
    location = np.zeros(2)
    location[0] = self.posx
    location[1] = self.posy
    end = np.zeros(2)
    end[0] = endx
    end[1] = endy
    starttime = self.environment.now
    angle = self.direction(location, end)
    print("Angle: ",angle)
    dist = np.linalg.norm(end - location)
    #culdist = starttime * velocity
    print("starttime:",starttime)
    culdist = 0
    E = 1000
    #culposition = start        
    #while( location[0] != end[0] and location[1] != end[1]):
    while( E >1): # E is an error function
        time = self.environment.now
        #print("Culdist: ",culdist)  
        print("time:",time)    
        culdist = (time - starttime) * self.velocity                                
        location[0] = location[0] + np.cos(angle)*culdist
        location[1] = location[1] + np.sin(angle)*culdist
        #if (ObsReport(location) = True):
        #    location[0] = self.posx       
        #    location[1] = self.posy       If a UAV finds an Obstraclu cansel move and avoid.
        #    location = avoid(location)
 
        self.posx = location[0]
        self.posy = location[1]
        #culdist = (time - starttime) * velocity    
        angle = self.direction(location, end)
        print("Angle: ",angle)          
        #print location
        print("location: ",location)
        E = np.linalg.norm(end - location)
        yield self.environment.timeout(0.5)

        #finally a UAV arrives at the destination by jumping(New change)
    time = self.environment.now
    location= end
    self.posx = end[0]
    self.posy = end[1]
    print(time)
    print("Goal!: ",location)
    
    
    

def ObsReport(location, obs): #obs = Obstracle(), location is a location of a UVA
    obspos = np.zeros(2)
    a = False
    for i in range(len(obs.obslist)):
        obspos[0] = obs.pos[0]
        obspos[1] = obs.pos[1]
        if (np.linalg.norm(obspos - location)<obs.radius):
            print("I'm in districted Area")
            a = True
            break
    return a


    