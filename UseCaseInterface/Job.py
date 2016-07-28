from math import sqrt
from UseCaseInterface.avoid import nextstep

'Class for the jobs created by the Use Cases which the UAVs work on'
class Job:

    def __init__(self, init_id, init_x, init_y, init_start_time, init_duration):
        self.id = init_id
        self.x = init_x
        self.y = init_y
        self.end_time = init_start_time + init_duration
        self.status = "Active"
        self.posx = self.x #Posx to be called from UI
        self.posy = self.y #Posy to be called from UI

    def check_time(self, time):
        if self.status == "Active":
            if self.end_time < time:
                self.time_out()
                return True
        return False

    def time_out(self):
        self.status = "Timed out"

    def finished(self):
        self.status = "Finished"

'''
Class for the Delivery Use Case jobs which are actual packages
Status: Laying around, In transit, Finished, Timed out
'''
class Delivery_Job(Job):

    def __init__(self, init_id, init_x, init_y, init_start_time, init_duration, init_xgoal, init_ygoal):
        Job.__init__(self, init_id, init_x, init_y, init_start_time, init_duration)
        self.destination_x = init_xgoal
        self.destination_y = init_ygoal
        self.status = "Laying around"
        self.type = "delivery"

    def check_time(self, time):
        if self.status == "Laying around" and self.end_time < time:
            self.time_out()
            return True
        else:
            return False

    def check_destination(self):
        if self.destination_x == self.x and self.destination_y == self.y:
            self.finished()
            return True
        else:
            return False

'''
Class for the Crowd Control Use Case jobs which are Crowd Events
Status: Active, Finished
Types: Panic, Illness, Disperse
'''
class Crowd_Job(Job):

   def __init__(self, init_id, init_x, init_y, init_start_time, init_duration, init_type):
       Job.__init__(self, init_id, init_x, init_y, init_start_time, init_duration)
       self.type = init_type

'''
Class for the Drone Defense jobs which are Hostile Drones
Status: Active, Finished
'''
class Defense_Job(Job):

    def __init__(self, init_id, init_x, init_y, init_start_time, init_duration, init_speed, init_xgoal, init_ygoal):
        Job.__init__(self, init_id, init_x, init_y, init_start_time, init_duration)
        self.speed = init_speed
        self.destination_x = init_xgoal
        self.destination_y = init_ygoal
        self.type = "defense"

    def check_UAV(self, x, y):
        dis = sqrt(((self.x - x)**2)+((self.y - y)**2))
        if self.speed >= dis:
            self.finished()
            return True
        else:
            return False

    def move(self):
        dis = sqrt(((self.x - self.destination_x)**2)+((self.y - self.destination_y)**2))
        if self.speed >= dis:
            self.failed()
            return True
        else:
            newpos = nextstep([self.x, self.y], [self.destination_x, self.destination_y], [], 1)
            self.x = newpos[0]
            self.y = newpos[1]
            return False

    def failed(self):
        self.status = "Failed"

'''
Class for the Advertisment Use Case jobs which are possible Advertisment locations
Status: Active, Started, Finished
'''
class Advert_Job(Job):

    def __init__(self, init_id, init_x, init_y, poslist,  init_start_time, init_duration):
        Job.__init__(self, init_id, init_x, init_y, init_start_time, init_duration)
        self.positions_final = poslist
        self.type = "advert"

    def check_uav_pos(self, positions):
        uav_counter = 0
        for pos in positions:
            if pos in self.positions_final:
                uav_counter += 1
        if uav_counter == 33:
            self.finished()
            return True
        else:
            return False

