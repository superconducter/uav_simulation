from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Simulation(models.Model):
    name=models.TextField(max_length=50)
    settings=models.TextField(max_length=50000)
    completed = models.BooleanField(blank=False, default=False)
    def __str__(self):
        return "{}: {}".format(self.id,self.name)

    def rounds_count(self):
        return self.rounds.count()

class Round(models.Model):
    simulation = models.ForeignKey(Simulation, related_name='rounds')
    round_number = models.IntegerField(default=0)

    def __str__(self):
        return str("({}){} Round: {}".format(self.simulation.id, self.simulation.name, self.round_number))
    class Meta:
        ordering = ('simulation','round_number',)

class Event(models.Model):
    round = models.ForeignKey(Round, related_name='events')
    name = models.TextField(max_length=50)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)

    def __str__(self):
        return "{}: {}".format(self.round, self.name)

class Agent(models.Model):
    '''
    We need to know which drone is which over multiple rounds. We need to make sure the sim team gives us this data
    '''
    round = models.ForeignKey(Round, related_name='agents')
    velocity = models.IntegerField(default=0)
    status = models.TextField()
    lat = models.FloatField()
    lng = models.FloatField()
    type = models.TextField(default="drone")
    identifier = models.IntegerField(default=0)
    def __str__(self):
        return "{}: {} {}: {}".format(self.round.simulation, self.round, self.type, self.status)

    class Meta:
        ordering = ('-round',)
        unique_together= ('round', 'identifier')

class Obstacle(models.Model):
    '''
    Can obstacles change during a simulation?
    '''
    borders = models.TextField() # Have no idea how to do this properly
    simulation = models.ForeignKey(Simulation)
