from django.conf.urls import url

from . import views

app_name = "events"
urlpatterns = [
    url(r'^all/$', views.EventsView.as_view(), name="events"),
    url(r'^add/$', views.add_event, name="add_event"),
]
