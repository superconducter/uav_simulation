"""
The DemoDataGenerator was initially created to generate some drone objects for testing the map in UI.
The DemoDataGenerator can be used for testing every use case, for scalability and for testing the performance. The DataGenerator creates agents (here: drones and static objects) and events. All agents have an initial position, a target position (only drones), a status (fly and land), an agent type, an agent name, and agent id. Events have a type, a name, and a position.
All of the information can be set in a setting file (look at config file).

How to use:
Start script directly!
In the first line in the command prompt, you can give the initial position.
In the second line, you can give the count of drones, the count of rounds and the count of all events, to generate the data for a use case. The data also can be used for statistics.

"""


import json
import os

import django
import numpy
import simpy
import time
from random import  randint
import random

from ui_sim_interface.interface import State, Event
from ui_sim_interface.pass_data import Observer

import logging



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ui.uavsim.settings")
django.setup()
from ui_sim_interface.models import Simulation, Agent


class Datagenerator:
    def __init__(self, name):
        sim = Simulation()
        sim.name = name
        sim.settings = open(os.path.dirname(os.path.realpath(__file__)) + "/demoDataGeneratorSettings.json", "r").read()
        sim.save()
        self.sim = sim
        self.state = State()
        self.observer = Observer()
        self.observer.new_simulation(self.state, sim.pk)
        self.agentTypes = ['default']
        self.eventTypes = ['default']
        self.staticTypes = []
        self.delay = 0

    def createDrones(self, num,maxRoundNums, pos_x,pos_y, numsOfEvents):
        i = 0

        posX = pos_x
        posY = pos_y
      

        droneList = []
        targetPos = []
        eventsToGenerate = numsOfEvents

        j=0
        tempEvents= 0
        roundNum = 0
        while roundNum < maxRoundNums:
            if roundNum == 0:
                while i < num:

                    randx = randint(0, 100)
                    randy = randint(0, 100)
                    targetPosX = randint(0, 100)
                    targetPosY = randint(0, 100)
                    #  print("tx: ",targetPosX, "  ty:",targetPosY)
                    drone = Agent()

                    drone.posx = posX
                    drone.posy = posY
                    drone.id = i
                    drone.type = random.choice(self.agentTypes)

                    # more than 50% of drones with status = 1
                    status = (i % 2)
                    if status == 0:
                        status = ((i + 1) + randint(0, 1)) % 2

                    drone.status = status

                    self.state.agents.append(drone)
                    droneList.append(drone)
                    targetPos.append((targetPosX, targetPosY))
                    posX = randx
                    posY = randy

                    i += 1

                self.state.fire()
                self.state.round_number += 1
                time.sleep(self.delay)

            if roundNum > 0:
                drone = Agent()
                tpx = 0
                tpy = 0
                index = 0

                for drone in droneList:
                    tuplePos = targetPos[index]
                    div = numpy.min([maxRoundNums, 20])
                    # percentProportion = numsOfEvents / div + (2 * roundNum) / div


                    tpx = int(tuplePos[0] / div)
                    tpy = int(tuplePos[1] / div)
                    # print("tx_final: ", tpx, " final_ty:", tpy)
                    drone.posx += tpx
                    drone.posy += tpy
                    index += 1


                if(eventsToGenerate > 0) :
                    #logging.debug("first if: ")
                    percentProportion = int(numsOfEvents / (maxRoundNums)) + ((2 * roundNum) / maxRoundNums)

                   # print("percentProportion",percentProportion)

                    while j < percentProportion and tempEvents < numsOfEvents:

                        self.createEvents()
                        tempEvents +=1
                        j+=1
                        eventsToGenerate -=1
                j=0

                if roundNum == 1:
                    self.create_static_agents()

                self.state.fire()
                self.state.round_number += 1

            roundNum += 1


    def createEvents(self):
        print("Start to create Events")

        event = Event()

        event_type = random.choice(self.eventTypes)
        event.type = event_type
        event.name = event_type

        event.posx = randint(0, 100)
        event.posy = randint(0, 100)

        self.state.events.append(event)

        print(event.type)


      #  self.state.fire()

    def create_static_agents(self, count=5):
        x = 0
        y = 0
        id = 0
        per_row = 5

        for agentType in self.staticTypes:
            if agentType['type'] == 'circle':
                x_margin = int(agentType['options']['radius']) * 2
                y_margin = x_margin
            elif agentType['type'] == 'rectangle':
                x_margin = int(agentType['options']['width']) * 2
                y_margin = int(agentType['options']['height']) * 2

            else:
                x_margin = 40
                y_margin = x_margin

            for i in range(count):
                agent = Agent()
                agent.posx = x
                agent.posy = y
                agent.id = id + 99999
                agent.type = agentType['name']
                agent.status = 1

                self.state.agents.append(agent)

                print('Added static agent with type {} at {};{}'.format(agentType['name'], x, y))

                x += x_margin
                id += 1

                if x > (x_margin * per_row):  # Line break
                    y += y_margin
                    x = 0

    def set_types_from_settings(self):
        settings = json.loads(self.sim.settings)
        # print(settings['ui'])

        self.eventTypes = []
        for event in settings['ui']['eventTypes']:
            self.eventTypes.append(event['name'])

        self.agentTypes = []
        self.staticTypes = []

        for agentType in settings['ui']['objectTypes']:
            if 'static' in agentType and agentType['static']:
                self.staticTypes.append(agentType)
            else:
                self.agentTypes.append(agentType['name'])

        print('Types from settings: \n- agents: {}\n- events: {}\n- static: {}'.format(self.agentTypes, self.eventTypes,
                                                                                       self.staticTypes))
        # exit(1)


def main():
    print("Start with data generator")

    input_position = input("Please enter start position: x,y ").split(',')
    if len(input_position) == 2:
        x, y = input_position
    else:
        x = 0
        y = 0

    pos_x = int(x)  # x Coordinate
    pos_y = int(y)  # y Coordinate

    drones, maxRounds,events = input("How many drones and rounds? : #Drones,#Rounds,#Events ").split(',')

    numsOfDrones = int(drones)
    maxRoundNums = int(maxRounds)
    numsOfEvents = int(events)

    dg = Datagenerator('Autogenerated simulation (agents={}, rounds={})'.format(numsOfDrones, maxRoundNums))
    dg.set_types_from_settings()
    #dg.agentTypes = ['uav', 'default', 'obstacle', 'base']

    dg.createDrones(numsOfDrones, maxRoundNums, pos_x, pos_y,numsOfEvents)


if __name__ == "__main__":
    # print("You should not call this script directly!")
    main()
