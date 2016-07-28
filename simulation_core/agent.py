#!/usr/bin/python
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Agent:

    def __init__(self, posx, posy, status=0, type="agent"):
        self.posx = posx
        self.posy = posy
        self.status = status
        self.type = type
        logging.debug("I am an Agent", [self.posx,self.posy])