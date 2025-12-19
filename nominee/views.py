from .models import *
from voting.models import *
from django.shortcuts import get_object_or_404, render, redirect
from itertools import groupby
from django.contrib import messages
from django.db import transaction
from itertools import groupby
from .models import Headline, Poll_information, Vote
from django.contrib.auth.decorators import login_required


def get_client_ip(request):
    """Get the client's IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def nominee_view(request, headline_id):
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
                if request.user.is_authenticated:
                    existing_votes = Vote.objects.filter(user=request.user, headline=headline)
                    existing_votes.delete()
                    for option_id in selected_options:
                        nominee = get_object_or_404(Poll_information, pk=option_id, headline=headline)
                        Vote.objects.create(user=request.user, poll_info=nominee, headline=headline)
                else:
                    ip_address = get_client_ip(request)
                    existing_votes = Vote.objects.filter(ip_address=ip_address, headline=headline)
                    if existing_votes.exists():
                        messages.warning(request, 'You have already voted from this location. Your previous vote has been updated.')
                    existing_votes.delete()
                    for option_id in selected_options:
                        nominee = get_object_or_404(Poll_information, pk=option_id, headline=headline)
                        Vote.objects.create(ip_address=ip_address, user= None, poll_info=nominee, headline=headline)
            messages.success(request, 'Your vote has been recorded successfully!')
            request.session['last_voted_headline'] = str(headline_id)
            return redirect('nominee:vote_success')
        except Exception as e:
            messages.error(request, f'An error occurred while recording your vote: {e}')
            return redirect('nominee:vote', headline_id=headline_id)
    nominees = Poll_information.objects.filter(headline=headline).only('id', 'sub_category', 'Name', 'headline').order_by('sub_category')
    grouped_nominees = [(sub_category, list(group)) for sub_category, group in groupby(nominees, key=lambda x: x.sub_category)]
    return render(request, 'nominee/voting_centre.html', {'headline': headline, 'grouped_nominees': grouped_nominees})


@login_required
def vote_success(request):
    headline_id = request.session.get('last_voted_headline')
    if headline_id:
        headline = get_object_or_404(Headline, id=headline_id)
        return render(request, 'nominee/vote_success.html', {'headline': headline})
    else:
        return redirect('nominee:vote')


@login_required
def nominee_logs(request, headline_id):
    headline = get_object_or_404(Headline, id=headline_id)
    nominees = Poll_information.objects.filter(headline=headline).only('id', 'sub_category', 'Name', 'headline').order_by('sub_category')
    votes_count = Vote.objects.filter(headline=headline).values('poll_info').annotate(vote_count=models.Count('id'))
    votes_dict = {vote['poll_info']: vote['vote_count'] for vote in votes_count}
    for nominee in nominees:
        nominee.vote_count = votes_dict.get(nominee.id, 0)
    grouped_nominees = [(sub_category, list(group)) for sub_category, group in groupby(nominees, key=lambda x: x.sub_category)]
    return render(request, 'nominee/nominee_logs.html', {'headline': headline, 'grouped_nominees': grouped_nominees})
                  