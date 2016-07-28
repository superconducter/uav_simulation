from random import randint
from UseCaseInterface.UAVFleet import UAVFleet
import UseCaseInterface.SensorData
import UseCaseInterface.avoid as Avoid
import logging
from math import sqrt


class DeliveryFleet(UAVFleet):
    def __init__(self, init_id, uavs, env):
        UAVFleet.__init__(self, init_id, uavs, env)
        self.uavstates = {}

    def calculate_step(self, jobs, time, sensor, speed, x, y):
        UAVFleet.calculate_step(self, time)
        for uav_id in self.UAV_ids:
            uav = self.world.getUAV(uav_id)

            jobposlist = []
            for job_id, job in jobs.items():
                if job.status == "Laying around":
                    jobposlist.append([job.x, job.y, job.status, job.id])

            uavpos = [uav.posx, uav.posy]
            if uav_id in self.uavstates:
                if self.uavstates[uav_id] == 0:  # If there a Job in the sensor data?
                    sensorjob = UseCaseInterface.SensorData.checkjobrange(jobposlist, uav.posx, uav.posy, speed)

                    if len(sensorjob) == 0:
                        pheromonelist = []
                        for pher_id, phero in self.pheromone.items():
                            pheromonelist.append([phero.x, phero.y])

                        uavdestination = [randint(0, x), randint(0, y)]
                        obslistchek = UseCaseInterface.SensorData.checksdobst(pheromonelist, uav.posx, uav.posy, speed, self.world)
                        move = Avoid.nextstep(uavpos, uavdestination, obslistchek, speed)
                        self.world.setnextmove(uav_id, move[0], move[1], speed)

                    else:
                        jobselect = UseCaseInterface.SensorData.selectjob(sensorjob, uav.posx, uav.posy, speed)
                        self.active_jobs[uav.id] = jobselect
                        self.uavstates[uav_id] += 1

                elif self.uavstates[uav_id] == 1:  # Move to the job
                    pheromonelist = [] #Pheromone gets ignored if there is a job in sensor range
                    for job_id, job in jobs.items():
                        if job.id == self.active_jobs[uav_id][3]:
                            uavdestination = [job.x, job.y]
                    if uavpos == uavdestination:
                        self.uavstates[uav_id] += 1
                    else:
                        obslistchek = UseCaseInterface.SensorData.checksdobst(pheromonelist, uav.posx, uav.posy, speed, self.world)
                        move = Avoid.nextstep(uavpos, uavdestination, obslistchek, speed)
                        self.world.setnextmove(uav_id, move[0], move[1], speed)


                elif self.uavstates[uav_id] == 2:  # Land
                    uav.status = 0
                    self.uavstates[uav_id] += 1

                elif self.uavstates[uav_id] == 3:  # Grap the Job and Start
                    for job_id, job in jobs.items():
                        if job_id == self.active_jobs[uav_id][3]:
                            job.status = "In transit"
                    uav.status = 1
                    self.uavstates[uav_id] += 1

                elif self.uavstates[uav_id] == 4:  # Move to the Job Destination
                    pheromonelist = [] #Pheromone gets ignored while moving towards the job destination
                    job = self.jobs[self.active_jobs[uav_id][3]]
                    job.x = uav.posx
                    job.y = uav.posy
                    uavdestination = [job.destination_x, job.destination_y]
                    if uavpos == uavdestination:
                        self.uavstates[uav_id] += 1
                    else:
                        obslistchek = UseCaseInterface.SensorData.checksdobst(pheromonelist, uav.posx, uav.posy, speed, self.world)
                        move = Avoid.nextstep(uavpos, uavdestination, obslistchek, speed)
                        self.world.setnextmove(uav_id, move[0], move[1], speed)

                elif self.uavstates[uav_id] == 5:  # Land
                    uav.status = 0
                    self.uavstates[uav_id] += 1

                elif self.uavstates[uav_id] == 6:  # Job Delivered
                    job = self.jobs[self.active_jobs[uav_id][3]]
                    if job.check_destination():
                        uav.status = 1
                        self.uavstates[uav_id] = 0
                    else:
                        uav.status = 1
                        self.uavstates[uav_id] = 4
                else:
                    self.uavstates[uav_id] = 0

            else:
                self.uavstates[uav_id] = 0

