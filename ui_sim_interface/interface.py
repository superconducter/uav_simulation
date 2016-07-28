"""
The interface was initially created to enable a common understanding on how objects should look.
Since Python supports duck-typing it was more important for the documentation thatn for the actual
implementation even though these objects can really be used as Source classes
"""
class Observable(object):
    """
    The observable can have a state and every time the state changes the Observers should be notified.
    Any object can be added with the subscribe function even though it should behave like an Observer.
    """
    def __init__(self):
        self.callbacks = []
    def subscribe(self, observable):
        self.callbacks.append(observable)
    def fire(self, **attrs):
        for observer in self.callbacks:
            try:
                observer.notify(self)
            except AttributeError as e:
                print("Error while notifying observer: ", e)

class Observer(object):
    """
    An observer is an object that can be notified of the state change of another object
    """
    def notify(self, observable):
        pass

class State(Observable):
    """
    A state is always the current state of the round. Once a round is finished, it is expected to fire and inform all
    its observers about the change.
    Having a mutable object as state is not a problem because only in the UI history must be kept.
    State should always be consistent at each fire event
    """
    def __init__(self):
        super().__init__()
        self.agents = list()
        self.events = list()
        self.round_number = 0

class Uav(object):
    def __init__(self):
        self.id = 0
        # Express direction and velocity as x | y coordinates? Why switch the represenation format.
        self.velocity = 0
        self.direction = 0
        #Possible status: on the ground: 0 | in the air: 1
        self.status = 0
        self.posx = 0
        self.posy = 0

class Event(object):
    def __init__(self):
        self.name = 'default'  # TODO Use name or type?
        self.type = 'default'  # Type || settingsconfig
        self.posx = 0
        self.posy = 0





