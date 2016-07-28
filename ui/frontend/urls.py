from django.conf.urls import url
from django.views.generic import TemplateView

"""
This file defines the URLs that are available at the root level (/)
"""
urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^settings', TemplateView.as_view(template_name="settingsView.html")),
    url(r'^logs', TemplateView.as_view(template_name="logs.html")),
]
