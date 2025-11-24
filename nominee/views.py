
from .models import *
from voting.models import *
from django.shortcuts import get_object_or_404, render, redirect
from itertools import groupby
from django.contrib import messages
from django.db import transaction
from itertools import groupby
from .models import Headline, Poll_information, Vote

def Nominee_view(request, headline_id):
    headline = get_object_or_404(Headline, id=headline_id)
    if request.method == 'POST':
        selected_options = []
        for key, value in request.POST.items():
            if key.startswith('option_') and value:
                selected_options.append(value)
        if not selected_options:
            messages.error(request, 'Please select at least one option before submitting your vote.')
            return redirect('nominee:vote', headline_id=headline_id)
        try:
            with transaction.atomic():
                existing_votes = Vote.objects.filter(user=request.user, headline=headline)
                existing_votes.delete()
                for option_id in selected_options:
                    nominee = get_object_or_404(Poll_information, pk=option_id, headline=headline)
                    Vote.objects.create(user=request.user, poll_info=nominee, headline=headline)
            messages.success(request, 'Your vote has been recorded successfully!')
            return redirect('nominee:vote_success')
        except Exception as e:
            messages.error(request, f'An error occurred while recording your vote: {e}')
            return redirect('nominee:vote', headline_id=headline_id)
    nominees = Poll_information.objects.filter(headline=headline).only('id', 'sub_category', 'Name', 'headline').order_by('sub_category')
    grouped_nominees = [
        (sub_category, list(group))
        for sub_category, group in groupby(nominees, key=lambda x: x.sub_category)
    ]
    return render(request, 'nominee/voting_centre.html', {'headline': headline, 'grouped_nominees': grouped_nominees})


def vote_success(request):
    return render(request, 'nominee/vote_success.html')


# def nominee_analysis(request, headline_id):
    # headline = get_object_or_404(Headline, id=headline_id)
    # nominees = Poll_information.objects.filter(headline=headline).only('id', 'sub_category', 'Name', 'headline').order_by('sub_category')
    # nominees_votes = nominees.annotate(vote_count=models.Count('vote'))                   
