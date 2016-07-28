

'Base Classes for Use Cases. Dont use! Rather use child!'
class UseCase:

    def __init__(self, init_x, init_y, init_id, env, control):
        self.uc_id = init_id
        self.x = init_x
        self.y = init_y
        self.world = env
        self.job_id = 0
        self.jobs = {}
        self.fleets = []
        self.control = control
