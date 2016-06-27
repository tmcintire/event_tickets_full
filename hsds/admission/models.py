from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum, F, Count


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    cash = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)

    def tickets(self):
        return self.tickets_set.all()

    def count(self):
        return self.tickets().aggregate(Count('type__type')).values()[0]

    def ad_type_count(self, type_id):
        return self.tickets().filter(type=type_id).aggregate(Count('type__type')).values()[0]

    def ad_type_total(self, type_id):
        return self.tickets().filter(type=type_id).aggregate(Sum(F('type__price'))).values()[0]

    def tickets_total(self):
        return self.tickets().aggregate(Sum(F('type__price'))).values()[0]

    def expenses(self):
        return self.expenses_set.all()

    def total_expenses(self):
        return self.expenses().aggregate(Sum(F('cost'))).values()[0]

    def __unicode__(self):
        return self.name


class AdmissionType(models.Model):
    type = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def ad_type(self):
        return self.tickets_set.all()

    def ad_type_total(self):
        return self.ad_type().aggregate(Count('type')).values()[0]

    def ad_type_total_price(self):
        return self.ad_type().aggregate(Sum(F('type__price'))).values()[0]

    def __unicode__(self):
        return '%s %s' % (self.type, self.price)


class Tickets(models.Model):
    type = models.ForeignKey(AdmissionType)
    event = models.ForeignKey(Event)

    def __unicode__(self):
        return '%s %s' % (self.type, self.event)


class Expenses(models.Model):
    name = models.ForeignKey(Event)
    type = models.CharField(max_length=100)
    notes = models.CharField(max_length=100)
    cost = models.DecimalField(max_length=10, decimal_places=2, max_digits=10)
    percent = models.IntegerField(max_length=3, blank=True, null=True)

    def __unicode__(self):
        return '%s %s' % (self.name, self.type)



