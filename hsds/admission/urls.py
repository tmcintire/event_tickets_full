from django.conf.urls import url

from . import views
from event.views import add_cash

app_name = "admission"
urlpatterns = [
    url(r'^(?P<event_id>[0-9]+)/$', views.admission_types, name="admission"),
    url(r'^(?P<event_id>[0-9]+)/addone/(?P<type_id>[0-9]+)/$', views.add_one, name="addone"),
    url(r'^(?P<event_id>[0-9]+)/deleteone/(?P<type_id>[0-9]+)/$', views.delete_one, name="deleteone"),
    url(r'^add/$', views.add_type, name="add_type"),
    url(r'^addexpense/$', views.add_expense, name="add_expense"),
    url(r'^addeventtype/$', views.add_event_type, name="add_event_type"),
    url(r'^addexpensetype/$', views.add_expense_type, name="add_expense_type"),
    url(r'^expenses/edit/(?P<expense_id>[0-9]+)/$', views.edit_expense, name="edit_expense"),
    url(r'^types/edit/(?P<i_id>[0-9]+)/$', views.edit_type, name="edit_type"),
    url(r'^(?P<event_id>[0-9]+)/cash/$', add_cash, name="starting_cash"),
]
