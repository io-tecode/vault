from urllib import request
from django.shortcuts import get_object_or_404, render
from voting.models import *


# Create your views here.
def Nominee_view(request, headline_id):
    headline = get_object_or_404(Headline, pk=headline_id)
    nominee = Poll_information.objects.filter(headline=headline).order_by('-creation_date') # Assume
    return render(request, 'nominee/voting_centre.html', {'headline': headline, 'nominee': nominee})