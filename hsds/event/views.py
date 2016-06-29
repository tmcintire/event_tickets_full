from django.shortcuts import render, get_object_or_404, render_to_response, RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from admission.models import Event
from forms import EventForm, CashForm
# Create your views here.


class EventsView(ListView):
    model = Event
    template_name = 'event_list.html'

    def get_context_data(self, **kwargs):
        context = super(EventsView, self).get_context_data(**kwargs)
        return context


def add_cash(request, event_id):
    instance = get_object_or_404(Event, pk=event_id)
    if request.POST:
            form = CashForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Modified!')
                return HttpResponseRedirect('/event/all/')
    else:
        form = CashForm(instance=instance)

    header = "You must enter a starting cash box amount"

    return render_to_response("add.html", {
        'form': form,
        'instance': instance,
        'header': header,
    }, context_instance=RequestContext(request))


def add_event(request):
    if request.POST:
            form = EventForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Task added!')
                return HttpResponseRedirect('/event/all/')
    else:
        form = EventForm()

    return render(request, 'add.html', locals())