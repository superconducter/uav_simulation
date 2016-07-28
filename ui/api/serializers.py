from rest_framework import serializers
from ui.api.fields import RawJsonField
from ui_sim_interface.models import Agent, Round, Simulation, Event
"""
Serializers are serialize and deserialize data from and to the API.
They define which fields should be converted and how foreign key relationships should be treated
"""

class AgentSerializer(serializers.ModelSerializer):
    round = serializers.ReadOnlyField(read_only=True, source='round.round_number')
    class Meta:
        model = Agent
        fields = ('identifier', 'status', 'velocity', 'lat', 'lng', 'round', 'type')

class AgentSparseSerializer(AgentSerializer):
    class Meta:
        fields = ('status', 'velocity', 'lat', 'lng', 'round', 'type')

class EventSerializer(serializers.ModelSerializer):
    round_number = serializers.IntegerField(source='round.round_number')

    class Meta:
        model = Event
        exclude= ('id',)

class RoundSerializer(serializers.ModelSerializer):
    drones = AgentSerializer(many=True, read_only=True)
    class Meta:
        model = Round
        fields = ('round_number', 'drones')

class SimulationSerializer(serializers.ModelSerializer):
    rounds = RoundSerializer(many=True, read_only=True)
    settings = RawJsonField()
    class Meta:
        model = Simulation
        fields = ('id','name', 'settings', 'rounds_count', 'rounds', 'completed')
