from django.shortcuts import get_object_or_404, render
from voting.models import *
from itertools import groupby
from urllib import request


# Create your views here.
def Nominee_view(request, headline_id):
    headline = get_object_or_404(Headline, pk=headline_id)
    nominee = Poll_information.objects.filter(headline=headline).order_by('sub_category')
    grouped_nominees = groupby(nominee, key=lambda x: x.sub_category)
    return render(request, 'nominee/voting_centre.html', {'headline': headline, 'nominee': nominee, 'grouped_nominees': grouped_nominees})