from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum, F, Count


class Organization(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class EventType(models.Model):
    event_type = models.CharField(max_length=100)

    def __unicode__(self):
        return self.event_type


class Event(models.Model):
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=100)
    type = models.ForeignKey(EventType)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    cash = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)

    def tickets(self):
        return self.tickets_set.all()

    # returns the count for all tickets sold of any type
    def count(self):
        return self.tickets_set.all().aggregate(Count('type__type')).values()[0]

    # returns the count for the specified type of admission
    def admission_type_count(self, type_id):
        return self.tickets_set.all().filter(type=type_id).aggregate(Count('type__type')).values()[0]

    # returns the total dollar amount of the specified type of admission
    def admission_type_total(self, type_id):
        return self.tickets_set.all().filter(type=type_id).aggregate(Sum(F('type__price'))).values()[0]

    def tickets_total(self):
        return self.tickets_set.all().aggregate(Sum(F('type__price'))).values()[0]

    def admission_types(self):
        return self.admissiontype_set.all()

    def admission_types_tickets(self, typeid):
        return self.tickets().filter(type=typeid)

    def expenses(self):
        return self.expenses_set.all()

    def expense_cost(self):
        return self.expenses().values("cost")

    def total_expenses(self):
        return self.expenses().aggregate(Sum(F('cost'))).values()[0]

    def __unicode__(self):
        return self.name


class AdmissionType(models.Model):
    event = models.ForeignKey(Event)
    type = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def admission_type(self):
        return self.tickets_set.all()

    def admission_type_count(self):
        return self.admission_type().aggregate(Count('type')).values()[0]

    def admission_type_total_price(self):
        return self.admission_type().aggregate(Sum(F('type__price'))).values()[0]

    def __unicode__(self):
        return '%s %s' % (self.type, self.price)


class Tickets(models.Model):
    type = models.ForeignKey(AdmissionType)
    event = models.ForeignKey(Event)

    def __unicode__(self):
        return '%s %s' % (self.type, self.event)


class ExpenseType(models.Model):
    expense_type = models.CharField(max_length=100)

    def __unicode__(self):
        return self.expense_type


class Expenses(models.Model):
    name = models.ForeignKey(Event)
    type = models.ForeignKey(ExpenseType)
    notes = models.CharField(max_length=100)
    cost = models.DecimalField(max_length=10, decimal_places=2, max_digits=10)
    percent = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return '%s %s' % (self.name, self.type)



