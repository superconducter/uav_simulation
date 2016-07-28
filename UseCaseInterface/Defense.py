from UseCaseInterface.UseCase import UseCase
from random import randint
from UseCaseInterface.Job import Defense_Job
from UseCaseInterface.DefenseFleet import DefenseFleet

'Jobs for the Defense Use Case. They get created with in defence area at random points'
class Defense(UseCase):

    def __init__(self, posx, posy, init_id, init_uavs, timestamp, env, control):
        self.number = init_uavs
        uav_ids = []
        UseCase.__init__(self, posx, posy, init_id, env, control)

        for n in range(init_uavs):
            new_uav_id = self.world.createUAV(self.x, self.y)
            uav_ids.append(new_uav_id)
            self.create_job(timestamp)

        self.fleets.append(DefenseFleet(0, self.x, self.y, uav_ids, self.world))

    def create_job(self, time):
        helpx = randint(self.x-25, self.x+25)
        helpy = randint(self.y-25, self.y+25)
        while self.control.check_space([[helpx, helpy]]) or helpx < 1 or helpy < 1:
            helpx = randint(self.x - 25, self.x + 25)
            helpy = randint(self.y - 25, self.y + 25)

        self.jobs[self.job_id] = Defense_Job(self.job_id, helpx, helpy, time, 1000, 1, self.x, self.y)
        #self.world.agents.append(self.jobs[self.job_id])
        self.control.event("Defense", "New")
        self.control.add_event(time, helpx, helpy, "DefenseNew")
        self.job_id +=1



    def calculate_action(self, time):
        while len(self.jobs) < self.number:
            self.create_job(time)

        for fleet in self.fleets:
            del_job = []
            for job_id, job in self.jobs.items():
                for uavid in fleet.UAV_ids:
                    uav = self.world.getUAV(uavid)
                    if job.check_UAV(uav.posx, uav.posy):
                        self.control.event("Defense", "Done")
                        self.control.add_event(time, uav.posx, uav.posy, "Defense Done")
                        del_job.append(job_id)

                    if job.status == "Active":
                        if job.move():
                            self.control.event("Defense", "Failed")
                            self.control.add_event(time, self.x, self.y, "Defense Failed")
                            del_job.append(job_id)

            for deljob in del_job:
                del self.jobs[deljob]

            fleet.calculate_step(self.jobs, time, self.control.sensor_range, self.control.uav_speed)

