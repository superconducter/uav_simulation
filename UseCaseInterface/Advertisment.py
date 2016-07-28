from UseCaseInterface.UseCase import UseCase
from UseCaseInterface.AdvertFleet import AdvertismentFleet
from UseCaseInterface.Job import Advert_Job
from random import randint

'Class for the advertisment jobs. For each job a single fleet gets created that then moves to the location'
class Advertisment(UseCase):

    def __init__(self, posx, posy, init_id, timestamp, env, control):
        UseCase.__init__(self, posx, posy, init_id, env, control)

        n_jobs = int((posx / 500) + (posy / 500))
        if n_jobs <= 0:
            posi = self.create_job(timestamp)
            help_x = randint(1, self.x)
            help_y = randint(1, self.y)
            poslist = []
            for n in range(33):
                poslist.append([help_x + n, help_y])
            while self.control.check_space(poslist):
                help_x = randint(1, self.x)
                help_y = randint(1, self.y)
                poslist = []
                for n in range(33):
                    poslist.append([help_x + n, help_y])
            uav_ids = []
            for pos in poslist:
                new_uav_id = self.world.createUAV(pos[0], pos[1])
                uav_ids.append(new_uav_id)
            new_fleet = AdvertismentFleet(self.job_id, help_x, help_y, uav_ids, self.world, self.jobs[self.job_id].x, self.jobs[self.job_id].y, posi)
            self.fleets.append(new_fleet)
            self.job_id += 1
        else:
            for n_j in range(n_jobs):
                posi = self.create_job(timestamp)
                help_x = randint(1, self.x)
                help_y = randint(1, self.y)
                poslist = []
                for n in range(33):
                    poslist.append([help_x + n, help_y])
                while self.control.check_space(poslist):
                    help_x = randint(1, self.x)
                    help_y = randint(1, self.y)
                    poslist = []
                    for n in range(33):
                        poslist.append([help_x + n, help_y])
                uav_ids = []
                for pos in poslist:
                    new_uav_id = self.world.createUAV(pos[0], pos[1])
                    uav_ids.append(new_uav_id)
                new_fleet = AdvertismentFleet(self.job_id, help_x, help_y, uav_ids, self.world,
                                              self.jobs[self.job_id].x, self.jobs[self.job_id].y, posi)
                self.fleets.append(new_fleet)
                self.job_id += 1

    def create_job(self, timestamp):
        help_x = randint(1, self.x)
        help_y = randint(1, self.y)
        positions_final = []
        positions_final.append([help_x, help_y])
        positions_final.append([help_x, help_y -2 ])
        positions_final.append([help_x , help_y+ 2])
        positions_final.append([help_x - 2, help_y + 2])
        positions_final.append([help_x -4, help_y + 2])
        positions_final.append([help_x- 4, help_y ])
        positions_final.append([help_x - 4, help_y - 2])
        positions_final.append([help_x + 2, help_y - 2])
        positions_final.append([help_x +4, help_y - 2])
        positions_final.append([help_x+4, help_y])
        positions_final.append([help_x + 4, help_y + 2])
        positions_final.append([help_x +4, help_y -7])
        positions_final.append([help_x, help_y - 7])
        positions_final.append([help_x, help_y - 9])
        positions_final.append([help_x, help_y - 5])
        positions_final.append([help_x - 4, help_y - 9])
        positions_final.append([help_x - 4, help_y - 5])
        positions_final.append([help_x +2, help_y - 9])
        positions_final.append([help_x + 2, help_y -5])
        positions_final.append([help_x -2, help_y - 9])
        positions_final.append([help_x - 2, help_y -5])
        positions_final.append([help_x + 4, help_y + 5])
        positions_final.append([help_x + 4, help_y + 7])
        positions_final.append([help_x + 4, help_y + 9])
        positions_final.append([help_x + 2, help_y + 5])
        positions_final.append([help_x + 2, help_y + 9])
        positions_final.append([help_x, help_y+5])
        positions_final.append([help_x, help_y+7])
        positions_final.append([help_x, help_y + 9])
        positions_final.append([help_x -2, help_y +5])
        positions_final.append([help_x -4, help_y +5])
        positions_final.append([help_x + 4, help_y - 5])
        positions_final.append([help_x + 4, help_y - 9])

        while self.control.check_space(positions_final):
            help_x = randint(1, self.x)
            help_y = randint(1, self.y)
            positions_final = []
            positions_final.append([help_x, help_y])
            positions_final.append([help_x, help_y - 2])
            positions_final.append([help_x, help_y + 2])
            positions_final.append([help_x - 2, help_y + 2])
            positions_final.append([help_x - 4, help_y + 2])
            positions_final.append([help_x - 4, help_y])
            positions_final.append([help_x - 4, help_y - 2])
            positions_final.append([help_x + 2, help_y - 2])
            positions_final.append([help_x + 4, help_y - 2])
            positions_final.append([help_x + 4, help_y])
            positions_final.append([help_x + 4, help_y + 2])
            positions_final.append([help_x + 4, help_y - 7])
            positions_final.append([help_x, help_y - 7])
            positions_final.append([help_x, help_y - 9])
            positions_final.append([help_x, help_y - 5])
            positions_final.append([help_x - 4, help_y - 9])
            positions_final.append([help_x - 4, help_y - 5])
            positions_final.append([help_x + 2, help_y - 9])
            positions_final.append([help_x + 2, help_y - 5])
            positions_final.append([help_x - 2, help_y - 9])
            positions_final.append([help_x - 2, help_y - 5])
            positions_final.append([help_x + 4, help_y + 5])
            positions_final.append([help_x + 4, help_y + 7])
            positions_final.append([help_x + 4, help_y + 9])
            positions_final.append([help_x + 2, help_y + 5])
            positions_final.append([help_x + 2, help_y + 9])
            positions_final.append([help_x, help_y + 5])
            positions_final.append([help_x, help_y + 7])
            positions_final.append([help_x, help_y + 9])
            positions_final.append([help_x - 2, help_y + 5])
            positions_final.append([help_x - 4, help_y + 5])
            positions_final.append([help_x + 4, help_y - 5])
            positions_final.append([help_x + 4, help_y - 9])

        new_job = Advert_Job(self.job_id, help_x, help_y, positions_final, timestamp, 1000)
        self.jobs[self.job_id] = new_job
        #self.world.agents.append(self.jobs[self.job_id])
        self.control.event("Advert", "New")
        self.control.add_event(timestamp, help_x, help_y, "AdvertNew")
        return positions_final

    def calculate_action(self, time):
        del_jobs = []
        fin_jobs = []
        for job_id, job in self.jobs.items():
            if job.status == "Active":
                if job.check_time(time):
                    del_jobs.append(job_id)
                    self.control.event("Advert", "Timed")
                else:
                    job.status = self.fleets[job_id].calculate_step(time)
                    positions = self.fleets[job_id].create_position_list()
                    if job.check_uav_pos(positions):
                        fin_jobs.append(job_id)
                        self.control.event("Advert", "Done")
            else:
                del_jobs.append(job_id)
                self.control.event("Advert", "Failed")

        for deljob in del_jobs:
            self.fleets[deljob].delete_uavs()
            del self.fleets[deljob]
            del self.jobs[deljob]

        for finjob in fin_jobs:
            del self.jobs[finjob]





