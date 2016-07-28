from django.contrib import admin
from django.contrib.admin import ModelAdmin
# Register your models here.
from ui_sim_interface.models import Agent, Simulation, Obstacle, Round, Event
"""
This file defines which models should be editable in the admin view at '/admin/'.
ModelAdmin provides a lot of basic functionality that is sufficient for basic CRUD tasks.
"""
admin.site.register(Agent, ModelAdmin)
admin.site.register(Round, ModelAdmin)
admin.site.register(Obstacle, ModelAdmin)
admin.site.register(Simulation, ModelAdmin)
admin.site.register(Event, ModelAdmin)