from UseCaseInterface.UAVFleet import UAVFleet
from math import sqrt
from random import randint
from UseCaseInterface.avoid import nextstep

class DefenseFleet(UAVFleet):

    def __init__(self, init_id, init_x, init_y, uavs, env):
        UAVFleet.__init__(self, init_id, uavs, env)
        self.x = init_x
        self.y = init_y

    def calculate_step(self, jobs, time, sensor, speed):
        UAVFleet.calculate_step(self, time)

        for uav_id in self.UAV_ids:
            uav = self.world.getUAV(uav_id)
            near_jobs = []
            for job_id, job in jobs.items():
                if sqrt((job.x - uav.posx) ** 2 + (job.y - uav.posy) ** 2) <= sensor: near_jobs.append(job)

            if len(near_jobs) == 0:
                self.world.setnextmove(uav_id, randint(self.x-25, self.x+25), randint(self.y-25, self.y+25))
            elif len(near_jobs) == 1:
                help_x = near_jobs[0].x
                help_y = near_jobs[0].y
                pos = nextstep([help_x, help_y],[self.x, self.y], [], 0.5)
                self.world.setnextmove(uav_id, pos[0], pos[1])

            else:
                ran_job = randint(0, len(near_jobs))
                help_x = near_jobs[ran_job].x
                help_y = near_jobs[ran_job].y
                pos = nextstep([help_x, help_y],[self.x, self.y], [], 0.5)
                self.world.setnextmove(uav_id, pos[0], pos[1])
