from django.contrib import messages
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.shortcuts import render, get_object_or_404, render_to_response, RequestContext
from django.contrib.auth.decorators import login_required
from forms import AdmissionForm, ExpenseForm, EventTypeForm, ExpenseTypeForm
from models import AdmissionType, Expenses, Tickets, Event
import json
from django.core.serializers.json import DjangoJSONEncoder


@login_required()
def admission_types(request, event_id):
    # Get all tickets that are related to the current event_id
    tickets = Tickets.objects.filter(event=event_id)

    # get all the event objects for this specific event
    event = Event.objects.get(pk=event_id)

    # Get all types for the event in question using the admission_types() method
    types = event.admission_types().order_by('-price')

    # define expenses and call the expenses() method from the Event Model which gets a list of all the expenses
    expenses = event.expenses()

    # runs the tickets_total() method from the Event model which gets all the tickets sold for the event
    total_revenue = event.tickets_total()

    cash = event.cash
    total_expenses = event.total_expenses()
    if total_revenue == None or total_expenses == None:
        cash_remaining = cash
    else:
        cash_remaining = ((total_revenue + cash) - total_expenses)

    # loops through the expenses list and modifies "cost" to the result of a percentage of total revenue
    for i in expenses:
        if i.percent > 0:
            i.cost = total_revenue * i.percent/100
            i.save()

    return render(request, "admissions.html", locals())


@login_required()
def add_one(request, event_id, type_id):
    new_ticket = Tickets(type_id=type_id, event_id=event_id)
    new_ticket.save()

    event = Event.objects.get(pk=event_id)
    count = event.admission_type_count(type_id)
    type_total = event.admission_type_total(type_id)
    tickets_total = event.tickets_total()
    tickets = event.count()
    cash = event.cash
    total_revenue = event.tickets_total()

    for i in event.expenses():
        i.cost = total_revenue * i.percent/100
        i.save()

    total_expenses = event.total_expenses()

    if total_revenue == None or total_expenses == None:
        cash_remaining = cash
    else:
        cash_remaining = total_revenue + cash - total_expenses
    expenses_query = event.expenses().values('cost')

    expenses = json.dumps(list(expenses_query), cls=DjangoJSONEncoder)

    data = {
        "count": count,
        "total": type_total,
        "tickets_total": tickets_total,
        "tickets_sold": tickets,
        "cash": cash,
        "cash_remaining": cash_remaining,
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "expenses": expenses,

    }

    return JsonResponse(data)


@login_required()
def delete_one(request, event_id, type_id):

    del_ticket = Tickets.objects.filter(type=type_id).latest('type')
    del_ticket.delete()

    event = Event.objects.get(pk=event_id)
    count = event.admission_type_count(type_id)
    type_total = event.admission_type_total(type_id)
    tickets_total = event.tickets_total()
    tickets = event.count()

    return JsonResponse({"count": count, "total": type_total, "tickets_total": tickets_total, "tickets_sold": tickets})


@login_required()
def add_type(request):
    if request.POST:
            form = AdmissionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Type added!')
                return HttpResponseRedirect('/event/all/')
    else:
        form = AdmissionForm()

    return render(request, 'add.html', locals())


@login_required()
def add_expense(request):
    if request.POST:
            form = ExpenseForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Expense added!')
                return HttpResponseRedirect('/event/all/')
    else:
        form = ExpenseForm()

    return render(request, 'add.html', locals())


@login_required()
def add_expense_type(request):
    if request.POST:
            form = ExpenseTypeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Expense type added!')
                return HttpResponseRedirect('/event/all/')
    else:
        form = ExpenseTypeForm()

    return render(request, 'add.html', locals())


@login_required()
def add_event_type(request):
    if request.POST:
            form = EventTypeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Event Type added!')
                return HttpResponseRedirect('/event/all/')
    else:
        form = EventTypeForm()

    return render(request, 'add.html', locals())


@login_required()
def edit_type(request, i_id):
    type = get_object_or_404(AdmissionType, pk=i_id)
    t = "Edit"

    if request.POST:
        form = AdmissionForm(request.POST, instance=type)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/event/all/')

    else:
        form = AdmissionForm(instance=type)

    return render_to_response("edit.html", {
        'form': form,
        'type': type,
    }, context_instance=RequestContext(request))


@login_required()
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expenses, pk=expense_id)
    t = "Edit"

    if request.POST:
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/event/all/')

    else:
        form = ExpenseForm(instance=expense)

    return render_to_response("edit.html", {
        'form': form,
        'expense': expense,
    }, context_instance=RequestContext(request))