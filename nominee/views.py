from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from voting.models import *
from itertools import groupby
from urllib import request
from django.contrib import messages
from django.shortcuts import redirect
from .models import *
from django.db import transaction, IntegrityError


# def Nominee_view(request, headline_id):
#     headline = get_object_or_404(Headline, pk=headline_id)

#     if request.method == 'POST':
#         selected_options = request.POST.getlist('option')
#         if not selected_options:
#             messages.error(request, 'Please select at least one option before submitting your vote.')
#             return redirect('nominee:vote', headline_id=headline_id)
#         if Vote.objects.filter(user=request.user, headline=headline).exists():
#             messages.error(request, 'You have already voted for this poll.')
#             return redirect('nominee:vote', headline_id=headline_id)
#         try:
#             with transaction.atomic():
#                 for option_id in selected_options:
#                     nominee = get_object_or_404(Poll_information, pk=option_id, headline=headline)
#                     Vote.objects.create(user=request.user, poll_info=nominee, headline=headline)  
#             messages.success(request, 'Your vote has been recorded successfully!')
#             return redirect('/voting/vote_success/') 
#             # return redirect('nominee:vote_success')
#         except IntegrityError as e:
#             messages.error(request, 'You have already voted for this poll.')
#             return redirect('nominee:vote', headline_id=headline_id)
#         except Exception as e:
#             messages.error(request, f'An error occurred while recording your vote: {str(e)}')
#             return redirect('nominee:vote', headline_id=headline_id)
#     nominees = Poll_information.objects.filter(headline=headline).only('id', 'sub_category', 'Name', 'headline').order_by('sub_category')
#     grouped_nominees = [
#         (sub_category, list(group))
#         for sub_category, group in groupby(nominees, key=lambda x: x.sub_category)
#     ]
#     return render(request, 'nominee/voting_centre.html', {'headline': headline, 'grouped_nominees': grouped_nominees})

def Nominee_view(request, headline_id):
    headline = get_object_or_404(Headline, pk=headline_id)
    
    if request.method == 'POST':
        selected_options = []
        for key, value in request.POST.items():
            if key.startswith('option_'):
                selected_options.append(value)
        if not selected_options:
            messages.error(request, 'Please select at least one option before submitting your vote.')
            return redirect('nominee:vote', headline_id=headline_id)
        if Vote.objects.filter(user=request.user, headline=headline).exists():
            messages.error(request, 'You have already voted for this poll.')
            return redirect('nominee:vote', headline_id=headline_id)
        try:
            with transaction.atomic():
                for option_id in selected_options:
                    nominee = get_object_or_404(Poll_information, pk=option_id, headline=headline)
                    Vote.objects.create(user=request.user, poll_info=nominee, headline=headline)
            messages.success(request, 'Your vote has been recorded successfully!')
            return redirect('nominee:vote_submission')
        except IntegrityError as e:
            messages.error(request, 'You have already voted for this poll.')
            return redirect('nominee:vote', headline_id=headline_id)
        except Exception as e:
            messages.error(request, f'An error occurred while recording your vote: {str(e)}')
            return redirect('nominee:vote', headline_id=headline_id)
    nominees = Poll_information.objects.filter(headline=headline).only('id', 'sub_category', 'Name', 'headline').order_by('sub_category')
    grouped_nominees = [
        (sub_category, list(group))
        for sub_category, group in groupby(nominees, key=lambda x: x.sub_category)
    ]
    return render(request, 'nominee/voting_centre.html', {'headline': headline, 'grouped_nominees': grouped_nominees})



def vote_success(request):
    return render(request, 'nominee/vote_success.html')
    # return redirect('voting:vote_submission', pk=request.GET.get('headline_id'))