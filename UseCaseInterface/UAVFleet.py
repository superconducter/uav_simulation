from UseCaseInterface.Pheromone import Pheromone

class UAVFleet:
    def __init__(self, init_id, uavs, env):
        self.id = init_id
        self.UAV_ids = uavs
        self.world = env
        self.pheromone = {}
        self.pherid = 0
        self.active_jobs = {}

    def calculate_step(self, time):
        del_pher_list = []
        for pher_id, pher in self.pheromone.items():
            if pher.check(time) == 0: del_pher_list.append(pher_id)

        for delpher in del_pher_list:
            del self.pheromone[delpher]

    def delete_uavs(self):
        for uav in self.UAV_ids:
            self.world.removeUAV(uav)
