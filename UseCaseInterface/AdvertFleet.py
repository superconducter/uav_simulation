from UseCaseInterface.UAVFleet import UAVFleet
import logging

'Fleet for the actions of the advertisment'
class AdvertismentFleet(UAVFleet):

    def __init__(self, init_id, x, y, uavs, env, goalx, goaly, posi):
        UAVFleet.__init__(self, init_id, uavs, env)
        self.goal_x = goalx
        self.goal_y = goaly
        self.current_goals = {}

        for n in range(33):
            self.current_goals[uavs[n]] = [self.goal_x, self.goal_y]

        self.positions_final = posi


    def calculate_step(self, time):
        UAVFleet.calculate_step(self, time)
        uav_count = 33
        for uav_id in self.UAV_ids:
            uav = self.world.getUAV(uav_id)
            if uav.status == 2: uav_count -= 1
            pos = [uav.posx, uav.posy]
            if pos in self.positions_final:
                self.check_next_empty(uav_id, pos)
            self.world.setnextmove(uav_id, self.current_goals[uav_id][0], self.current_goals[uav_id][1])

        if uav_count == 33:
            return "Active"
        else:
            return "Failed"

    def create_position_list(self):
        position_list = []
        for uav_id in self.UAV_ids:
            uav = self.world.getUAV(uav_id)
            position_list.append([uav.posx, uav.posy])
        return position_list

    def check_next_empty(self, uav, pos):
        posnr = [i for i,x in enumerate(self.positions_final) if x == pos]
        next_pos = posnr[0] + 1
        if next_pos == 33:
            return
        else:
            list = self.create_position_list()
            if self.positions_final[next_pos] in list:
                return
            else:
                self.current_goals[uav] = self.positions_final[next_pos]



