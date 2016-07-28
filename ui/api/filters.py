import django_filters

from ui_sim_interface.models import Simulation


class SimulationFilter(django_filters.FilterSet):
    class Meta:
        model = Simulation
        fields = {'name': ['exact', 'icontains'],
                 }