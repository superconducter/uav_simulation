'Class to simulate the pheromone of ants'
class Pheromone:

    'Pheromone gets created with a position and a duration'
    def __init__(self, init_id, init_x, init_y, timestamp, duration):
        self.id = init_id
        self.x = init_x
        self.y = init_y
        self.end = timestamp + duration

    'Either the pheromone has some time left that is returned or it has faded'
    def check(self, time):
        if (time < self.end): return self.end - time
        else: return 0

    'Renews old pheromone if an UAV passes there'
    def renew(self, time, duration):
        if (self.end < time + duration): self.end = time + duration