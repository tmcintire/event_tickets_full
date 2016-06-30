from models import Organization


def organization(request):
    # This needs to be organized in some way to allow multiple organizations to have multiple events
    organization_name = Organization.objects.get(pk=1)

    if organization_name is None:
        organization_name = "Event Organizer"
    return locals()
