from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    cash = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)

    def __unicode__(self):
        return self.name
