from django.contrib import messages
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, render_to_response, RequestContext
from forms import AdmissionForm, ExpenseForm
from models import AdmissionType, Expenses, Tickets, Event


def admission_types(request, event_id):
    # Get all tickets that are related to the current event_id
    tickets = Tickets.objects.filter(event=event_id)

    # Get all types from the database, this needs to show types only for the specific event
    types = AdmissionType.objects.all()

    # get all the event objects for this specific event
    event = Event.objects.get(pk=event_id)

    # define expenses and call the expenses() method from the Event Model which gets a list of all the expenses
    expenses = event.expenses()

    # runs the tickets_total() method from the Event model which gets all the tickets sold for the event
    total_revenue = event.tickets_total()

    cash = event.cash
    cash_remaining = (total_revenue + cash - event.total_expenses())

    # loops through the expenses list and modifies "cost" to the result of a percentage of total revenue
    for i in expenses:
        if i.percent > 0:
            i.cost = total_revenue * i.percent/100
            i.save()

    return render(request, 'admissions.html', locals())


def add_one(request, event_id, type_id):
    new_ticket = Tickets(type_id=type_id, event_id=event_id)
    new_ticket.save()

    event = Event.objects.get(pk=event_id)
    count = event.ad_type_count(type_id)
    type_total = event.ad_type_total(type_id)
    tickets_total = event.tickets_total()
    tickets = event.count()

    return JsonResponse({"count": count, "total": type_total, "tickets_total": tickets_total, "tickets_sold": tickets})


def delete_one(request, event_id, type_id):

    del_ticket = Tickets.objects.filter(type=type_id).latest('type')
    del_ticket.delete()

    event = Event.objects.get(pk=event_id)
    count = event.ad_type_count(type_id)
    type_total = event.ad_type_total(type_id)
    tickets_total = event.tickets_total()
    tickets = event.count()

    return JsonResponse({"count": count, "total": type_total, "tickets_total": tickets_total, "tickets_sold": tickets})


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