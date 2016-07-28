import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

'Internal collection about the statistics of the jobs. Can be used to test if Use Cases and behavior work'
class UseCaseStatistic:
    def __init__(self):
        self.advert_create = 0
        self.advert_done = 0
        self.advert_timed = 0
        self.advert_failed = 0
        self.deliver_create = 0
        self.deliver_done = 0
        self.deliver_timed = 0
        self.deliver_failed = 0
        self.defense_create = 0
        self.defense_done = 0
        self.defense_failed = 0

    def job_created(self, type):
        if type == "Advert":
            self.advert_create += 1
        elif type == "Delivery":
            self.deliver_create += 1
        elif type == "Defense":
            self.defense_create += 1
        else:
            pass

    def job_done(self, type):
        if type == "Advert":
            self.advert_done += 1
        elif type == "Delivery":
            self.deliver_done += 1
        elif type == "Defense":
            self.defense_done += 1
        else:
            pass

    def job_timed(self, type):
        if type == "Advert":
            self.advert_timed += 1
        elif type == "Delivery":
            self.deliver_timed += 1
        else:
            pass

    def job_failed(self, type):
        if type == "Advert":
            self.advert_failed += 1
        elif type == "Delivery":
            self.deliver_failed += 1
        elif type == "Defense":
            self.defense_failed += 1
        else:
            pass

    '''Statistics get logged in that order for Advertisement Jobs created, finished, timed out and failed, for Delivery
    jobs created, finished, timed out and failed and for Defense jobs created, finished and failed'''
    def return_stats(self):
        logging.debug([self.advert_create, self.advert_done, self.advert_timed, self.advert_failed, self.deliver_create, self.deliver_done,
                self.deliver_timed, self.deliver_failed, self.defense_create, self.defense_done, self.defense_failed])
