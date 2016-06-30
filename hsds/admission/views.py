from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, render_to_response, RequestContext, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from forms import *
from models import AdmissionType, Expenses, Tickets, Event, ExpenseType, Income, IncomeType
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

    income = event.income()
    total_income = event.total_income()

    # runs the tickets_total() method from the Event model which gets all the tickets sold for the event
    total_revenue = event.tickets_total()

    if total_income is None:
        all_income = total_revenue
    else:
        all_income = total_income + total_revenue

    cash = event.cash
    total_expenses = event.total_expenses()
    if total_revenue is None or total_expenses is None:
        cash_remaining = cash
    else:
        cash_remaining = ((all_income + cash) - total_expenses)

    # loops through the expenses list and modifies "cost" to the result of a percentage of total revenue
    if total_revenue is not None:
        for i in expenses:
            if i.percent > 0:
                i.cost = total_revenue * i.percent/100
                i.save()

    return render(request, "admissions.html", locals())


def report(request):

    events = Event.objects.all()
    header = "Reports"

    return render(request, "report.html", locals())


@login_required()
def add_tickets(request, event_id):

    if request.method == 'POST':

        # Get post data from the form submit, along with the admission type clicked
        num_tickets = request.POST.get('ticket_number')
        type_id = request.POST.get('type_id')

        #Create new tickets corresponding with number of tickets chosen
        i = 0
        while i < int(num_tickets):
            i += 1
            new_ticket = Tickets(type_id=type_id, event_id=event_id)
            new_ticket.save()

        # Grab data from database to be passed back to the template

        event = Event.objects.get(pk=event_id)
        count = event.admission_type_count(type_id)
        type_total = event.admission_type_total(type_id)
        tickets_total = event.tickets_total()
        tickets = event.count()
        cash = event.cash
        total_income = event.total_income()
        total_revenue = event.tickets_total()

        if total_income is None:
            all_income = total_revenue
        else:
            all_income = total_income + total_revenue

        for i in event.expenses():
            if i.percent != 0:
                i.cost = total_revenue * i.percent / 100
                i.save()

        total_expenses = event.total_expenses()

        if total_revenue is None or total_expenses is None:
            cash_remaining = cash
        else:
            cash_remaining = all_income + cash - total_expenses
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
            "all_income": all_income,
            "expenses": expenses,
            "result": "Successful",
            "num_tickets": num_tickets,
            "type_id": type_id,
            "event_id": event_id,


        }



        # response_data = {}
        #
        # response_data['result'] = 'Create post successful!'
        # response_data['num_tickets'] = num_tickets
        # response_data['type_id'] = type_id
        # response_data['event_id'] = event_id





        return JsonResponse(data)

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


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
def add_type(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.POST:
            form = AdmissionForm(request.POST)
            if form.is_valid():
                form.save()
                url = reverse('admission:add_type', args=(event.id,))
                return HttpResponseRedirect(url)
    else:
        event_name = event.id
        data_dict = {'event': event_name}
        form = AdmissionForm(initial=data_dict)

    title = "Admission Types"
    data = AdmissionType.objects.filter(event=event_id).order_by('-price')

    return render(request, 'add.html', locals())


@login_required()
def add_expense(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.POST:
            form = ExpenseForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Expense added!')
                url = reverse('admission:add_expense', args=(event.id,))
                return HttpResponseRedirect(url)
    else:
        event_name = event.id
        data_dict = {'name': event_name, 'cost': '0'}
        form = ExpenseForm(initial=data_dict)

    title = "Expenses"
    data = Expenses.objects.filter(name=event_id)

    return render(request, 'add.html', locals())


@login_required()
def add_expense_type(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.POST:
            form = ExpenseTypeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Expense type added!')
                url = reverse('admission:add_expense_type', args=(event.id,))
                return HttpResponseRedirect(url)
    else:
        event_name = event.id
        data_dict = {'event': event_name}
        form = ExpenseTypeForm(initial=data_dict)

    data = ExpenseType.objects.all()
    title = "Expense Types"

    return render(request, 'add.html', locals())


@login_required()
def add_income(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.POST:
            form = IncomeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Income added!')
                url = reverse('admission:add_income', args=(event.id,))
                return HttpResponseRedirect(url)
    else:
        event_name = event.id
        data_dict = {'event': event_name}
        form = IncomeForm(initial=data_dict)

    title = "Income"
    data = Income.objects.filter(event=event_id)

    return render(request, 'add.html', locals())


@login_required()
def add_income_type(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.POST:
            form = IncomeTypeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Income type added!')
                url = reverse('admission:add_income_type', args=(event.id,))
                return HttpResponseRedirect(url)
    else:
        event_name = event.id
        data_dict = {'event': event_name}
        form = IncomeTypeForm(initial=data_dict)

    data = IncomeType.objects.filter(event=event_id)
    title = "Income Types"

    return render(request, 'add.html', locals())



@login_required()
def add_event_type(request):
    if request.POST:
            form = EventTypeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Event Type added!')
                return HttpResponseRedirect('/events/')
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

            return HttpResponseRedirect('/events/')

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

            return HttpResponseRedirect('/events/')

    else:
        form = ExpenseForm(instance=expense)

    return render_to_response("edit.html", {
        'form': form,
        'expense': expense,
    }, context_instance=RequestContext(request))