from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from voting.models import *
from itertools import groupby
from urllib import request
from django.contrib import messages
from django.shortcuts import redirect


def Nominee_view(request, headline_id):
    headline = get_object_or_404(Headline, pk=headline_id)
    
    if request.method == 'POST':
        selected_options = request.POST.getlist('option')
        if not selected_options:
            pass
        else:
            for option_id in selected_options:
                try:
                    nominee = Poll_information.objects.get(pk=option_id)
                    print(f"Vote recorded for: {nominee.Name}")
                except Poll_information.DoesNotExist:
                    return HttpResponse("Nominee not found.", status=404)
            messages.success(request, 'Your vote has been recorded successfully!')
            return redirect('nominee_view', headline_id=headline_id)
    nominees = Poll_information.objects.filter(headline=headline).only('id', 'sub_category', 'Name', 'headline').order_by('sub_category')
    grouped_nominees = [
        (sub_category, list(group)) 
        for sub_category, group in groupby(nominees, key=lambda x: x.sub_category)
    ]
    return render(request, 'nominee/voting_centre.html', {'headline': headline, 'grouped_nominees': grouped_nominees})