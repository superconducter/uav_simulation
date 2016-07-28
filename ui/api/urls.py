from django.conf.urls import url, include
from rest_framework import routers

from ui.api.views import EventView, StatisticsView, AgentView
from . import views

"""
Here all URLs that are available in the API are defined.
"""

# A router can be used to define an entire viewset including detail views.
router = routers.DefaultRouter()
router.register(r'agents', views.AgentViewset)
router.register(r'rounds', views.RoundViewset)
router.register(r'simulations', views.SimulationViewset)
router.register(r'events', views.EventViewset)

urlpatterns = [
    url(r'^simulations/run$', views.start_simulation),
    url(r'^', include(router.urls)),
    url(r'^events2', EventView.as_view()),#TODO remove the '2'
    url(r'^agents2', AgentView.as_view()),#TODO remove the '2'
    url(r'^statistics', StatisticsView.as_view()),
]
