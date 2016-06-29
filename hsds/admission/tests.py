from django.test import TestCase
from models import AdmissionType
# Create your tests here.

from models import Event

event = Event.objects.get(pk=1)

