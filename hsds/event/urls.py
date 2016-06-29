from django.conf.urls import url

from . import views
from admission.views import add_event_type

app_name = "events"
urlpatterns = [
    url(r'^add/$', views.add_event, name="add_event"),
    url(r'^addeventtype/$', add_event_type, name="add_event_type"),
]
