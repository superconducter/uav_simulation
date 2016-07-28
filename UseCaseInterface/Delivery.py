from UseCaseInterface.UseCase import UseCase
from random import randint
from UseCaseInterface.DeliveryFleet import DeliveryFleet
from UseCaseInterface.Job import Delivery_Job

'''
Job = Package
Fleet = One Fleet per Delivery Provider, Usually two fleets
'''
class Delivery(UseCase):

    def __init__(self, posx, posy, init_id, init_uavs, list_coord_uav, timestamp, env, control):
        self.job_id = 0
        uav_ids = []
        UseCase.__init__(self, posx, posy, init_id, env, control)

        if len(list_coord_uav) == init_uavs:
            for n in range(init_uavs):
                new_uav_id = self.world.createUAV(list_coord_uav[n][0], list_coord_uav[n][1])
                uav_ids.append(new_uav_id)
        else:
            for n in range(init_uavs):
                new_uav_id = self.world.createUAV(randint(1, self.x), randint(1, self.y))
                uav_ids.append(new_uav_id)

        'Split the UAVs up between the two delivery providers'
        if len(uav_ids) == 1:
            self.fleets.append(DeliveryFleet(1, uav_ids, self.world))
        else:
            self.fleets.append(DeliveryFleet(1, uav_ids[:len(uav_ids)//2], self.world))
            self.fleets.append(DeliveryFleet(2, uav_ids[len(uav_ids)//2:], self.world))

        'Create a number of jobs depending on the size of the map, with one job minimum'
        n_jobs = int((posx/100) + (posy/100)) + init_uavs
        if n_jobs <= 0:
            self.create_job(timestamp)
        else:
            for n in range(n_jobs):
                self.create_job(timestamp)

    'Function to create and place jobs'
    def create_job(self, timestamp):
        help_x = randint(1, self.x)
        help_y = randint(1, self.y)
        new_job = Delivery_Job(self.job_id, help_x, help_y, timestamp, 1000,
                               randint(1, self.x), randint(1, self.y))
        self.jobs[self.job_id] = new_job
        #self.world.agents.append(self.jobs[self.job_id])
        self.control.add_event(timestamp, help_x, help_y, "DeliveryNew")
        self.job_id += 1
        self.control.event("Delivery", "New")



    def calculate_action(self, time):
        sensor = self.control.sensor_range
        speed = self.control.uav_speed
        del_jobs = []
        for job_id, job in self.jobs.items():
            if job.check_destination():
                self.control.event("Delivery", "Done")
                self.control.add_event(time, job.destination_x, job.destination_y, "DeliveryDone")
                del_jobs.append(job_id)
            else:
                if job.check_time(time):
                    self.control.event("Delivery", "Timed")
                    self.control.add_event(time, job.x, job.y, "DeliveryTimed")
                    del_jobs.append(job_id)

        for deljob in del_jobs:
            del self.jobs[deljob]

        for fleet in self.fleets:
            fleet.calculate_step(self.jobs, time, sensor, speed, self.x, self.y)


