# Create your views here.
import json
import os
import subprocess

import sys
from django.http import HttpResponseBadRequest
from rest_framework.decorators import detail_route, api_view, parser_classes
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from ui.api.filters import SimulationFilter
from ui.api.paginations import LargeResultsSetPagination, BareLimitOffsetPagination
from ui_sim_interface.models import Agent, Round, Simulation, Event
from .serializers import AgentSerializer, RoundSerializer, SimulationSerializer, EventSerializer




class AgentViewset(ReadOnlyModelViewSet):
    """
    API endpoint that allows Agents to be retrieved.
    """
    queryset = Agent.objects.all().order_by('round_id')
    authentication_classes = []
    permission_classes = []
    pagination_class = BareLimitOffsetPagination
    serializer_class = AgentSerializer
    filter_fields = ('status', 'lat', 'lng', 'round', 'round__simulation')

class RoundViewset(ReadOnlyModelViewSet):
    """
    API endpoint that allows Rounds to be retrieved.
    """
    authentication_classes = []
    permission_classes = []
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('id', 'round_number', 'simulation')

    @detail_route(url_path='drones')
    def list_drones(self, request, pk=None):
        dvs = AgentViewset()
        return dvs.list(request=request, pk=pk)

    @detail_route()
    def events(self, request, pk=None):
        dvs = EventViewset.as_view({'get': 'list'})
        dvs.cls.queryset = dvs.cls.queryset.filter(round_id=int(pk))
        return dvs(request)

class SimulationViewset(ModelViewSet):
    """
    Lists all the simulations
    """
    pagination_class = BareLimitOffsetPagination
    authentication_classes = []
    permission_classes = []
    queryset = Simulation.objects.order_by('-pk')
    serializer_class = SimulationSerializer
    filter_class = SimulationFilter

    @detail_route()
    def rounds(self, request, pk=None):
        dvs = RoundViewset.as_view({'get': 'list'})
        dvs.cls.queryset = dvs.cls.queryset.filter(simulation_id=int(pk))
        return dvs(request)

class EventView(APIView):
    """
    Returns all the events for a simulation
    """
    def get(self, request, format=None):
        ret = []
        events = Event.objects.all()
        last_round = -1
        simulation_id = request.query_params.get('simulation', None)
        if simulation_id:
            events = Event.objects.filter(round__simulation=simulation_id).order_by('round')
        else:
            return HttpResponseBadRequest("GET parameter simulation is missing.")
        for event in events:
            if event.round.round_number > last_round:
                last_round = event.round.round_number
                ret.append({
                    'round_number': event.round.round_number,
                    'events': []
                })
            ret[-1]['events'].append({"type": event.name,
                           "location": [event.lat, event.lng]})
        return Response(ret)

class AgentView(APIView):
    """
    Returns all the events for a simulation
    """
    def get(self, request, format=None):
        ret = {}
        agents = None
        simulation_id = request.query_params.get('simulation', None)
        if simulation_id:
            agents = Agent.objects.filter(round__simulation=simulation_id).order_by('round').select_related('round')
        else:
            return HttpResponseBadRequest("GET parameter simulation is missing.")
        for agent in agents:
            agent_representation = ret.setdefault(agent.identifier, {'coordinates': [],
                                              'status': [],
                                              'round': [],
                                              'type': agent.type})
            agent_representation['coordinates'].append([agent.lng, agent.lat])
            agent_representation['status'].append(agent.status)
            agent_representation['round'].append(agent.round.round_number)
            #AgentSerializer(agent).data)
        return Response(ret)

class StatisticsView(APIView):
    """
    Returns basic statistics for the index page.
    """
    def get(self, request, format=None):
        ret = {}
        ret['events'] = Event.objects.all().count()
        ret['agents'] = Agent.objects.all().count()
        ret['simulations'] = Simulation.objects.all().count()
        ret['rounds'] = Round.objects.all().count()
        return Response(ret)

class EventViewset(ReadOnlyModelViewSet):
    """
    Showing all events. Show only events from all rounds number 2:
    ?round_round_number=2
    Show only events from simulation 2:
    ?round__simulation=1
    """
    queryset = Event.objects.all().order_by('round_id')
    authentication_classes = []
    pagination_class = LargeResultsSetPagination
    permission_classes = []
    serializer_class = EventSerializer
    filter_fields = ('lat', 'lng', 'round__round_number', 'round', 'round__simulation')


@api_view(['POST'])
@parser_classes((JSONParser,))
def start_simulation(request):
    """
    Pass an arbitrary JSON file that will be used as configuration during a simulation.
    The simulation will be started asynchronously and rounds will be added to that simulation
    as they are being processed.
    :param request:
    :return:
    """

    #Create simulation
    simulation = Simulation()
    try:
        simulation.name = request.data["name"]
        simulation.settings = json.dumps(request.data)
    except KeyError:
        return (HttpResponseBadRequest())
    simulation.save()

    #Start simulation and pass reference to simulation
    env= os.environ.copy()
    proc = subprocess.Popen([sys.executable, "ui/api/start_simulation.py", str(simulation.pk), json.dumps(request.data)], stdout=subprocess.PIPE, env=env)
    return (Response({'identifier': simulation.pk,
                      'received': request.data}))
