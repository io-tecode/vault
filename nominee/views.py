from .models import *
from voting.models import *
from django.shortcuts import get_object_or_404, render, redirect
from itertools import groupby
from django.contrib import messages
from django.db import transaction
from itertools import groupby
from django.views.decorators.csrf import csrf_protect
from .models import Headline, Poll_information, vote
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_protect
def nominee_view(request, headline_id):
    headline = get_object_or_404(Headline, id=headline_id)
    if not headline.allow_vote_changes:
        messages.info(request, 'Vote changes are already disabled for this poll.')
        return redirect('nominee:vote_success')
    if headline.require_google_auth:
        if not request.user.is_authenticated:
            request.session['next_vote_url'] = request.path
            messages.info(request, 'Please sign in with Google to vote in this poll.')
            return redirect('google_oauth_vote', headline_id=headline_id)
        has_google = SocialAccount.objects.filter(user=request.user, provider='google').exists()
        if not has_google:
                request.session['next_vote_url'] = request.path
                messages.warning(request, 'This poll requires Google authentication. Please link your Google account.')
                return redirect('google_oauth_vote', headline_id=headline_id)
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
                    existing_votes = vote.objects.filter(user=request.user, headline=headline)
                    if existing_votes.filter(is_locked=True).exists():
                        messages.warning(request, 'Your vote is locked and cannot be changed.')
                        request.session['last_voted_headline'] = str(headline_id)
                        return redirect('nominee:vote_success')
                    existing_votes.delete()
                    for option_id in selected_options:
                        nominee = get_object_or_404(Poll_information, pk=option_id, headline=headline)
                        vote.objects.create(user=request.user, poll_info=nominee, headline=headline)
                else:
                    if headline.require_google_auth:
                        messages.error(request, 'Google authentication required to vote.')
                        return redirect('google_oauth_vote', headline_id=headline_id)
                    ip_address = get_client_ip(request)
                    existing_votes = vote.objects.filter(ip_address=ip_address, headline=headline)
                    if existing_votes.filter(is_locked=True).exists():
                        messages.warning(request, 'Your vote is locked and cannot be changed.')
                        request.session['last_voted_headline'] = str(headline_id)
                        return redirect('nominee:vote_success')
                    if existing_votes.exists():
                        messages.warning(request, 'You have already voted from this location. Your previous vote has been updated.')
                    existing_votes.delete()
                    for option_id in selected_options:
                        nominee = get_object_or_404(Poll_information, pk=option_id, headline=headline)
                        vote.objects.create(ip_address=ip_address, poll_info=nominee, headline=headline)
            messages.success(request, 'Your vote has been recorded successfully!')
            request.session['last_voted_headline'] = str(headline_id)
            return redirect('nominee:vote_success')
        except Exception as e:
            messages.error(request, f'An error occurred while recording your vote: {e}')
            return redirect('nominee:vote', headline_id=headline_id)
    has_voted, is_vote_locked = False, False
    if request.user.is_authenticated:
        user_votes = vote.objects.filter(user=request.user, headline=headline)
        has_voted, is_vote_locked = user_votes.exists(), user_votes.filter(is_locked=True).exists()
    else:
        ip_address = get_client_ip(request)
        ip_votes = vote.objects.filter(ip_address=ip_address, headline=headline)
        has_voted, is_vote_locked = ip_votes.exists(), ip_votes.filter(is_locked=True).exists()
    nominees = Poll_information.objects.filter(headline=headline).only('id', 'sub_category', 'Name', 'headline').order_by('sub_category')
    grouped_nominees = [(sub_category, list(group)) for sub_category, group in groupby(nominees, key=lambda x: x.sub_category)]
    return render(request, 'nominee/voting_centre.html', {'headline': headline, 'grouped_nominees': grouped_nominees, 'has_voted': has_voted, 'is_vote_locked': is_vote_locked})


@csrf_protect
def vote_success(request):
    headline_id = request.session.get('last_voted_headline')
    if headline_id:
        headline = get_object_or_404(Headline, id=headline_id)
        vote_locked = False
        if request.user.is_authenticated:
            vote_locked = vote.objects.filter(
                user=request.user, 
                headline=headline, 
                is_locked=True
            ).exists()
        else:
            ip_address = get_client_ip(request)
            vote_locked = vote.objects.filter(
                ip_address=ip_address, 
                headline=headline, 
                is_locked=True
            ).exists()
        
        from django.utils import timezone
        context = {
            'headline': headline,
            'vote_locked': vote_locked,
            'now': timezone.now()
        }
        return render(request, 'nominee/vote_success.html', context)
    else:
        if not headline_id:
            messages.info(request, 'No recent voting activity found.')
            return redirect('nominee:vote_success')
        else:
            return redirect('nominee:vote')


@csrf_protect
def nominee_logs(request, headline_id):
    headline = get_object_or_404(Headline, id=headline_id)
    nominees = Poll_information.objects.filter(headline=headline).only('id', 'sub_category', 'Name', 'headline').order_by('sub_category')
    votes_count = vote.objects.filter(headline=headline).values('poll_info').annotate(vote_count=models.Count('id'))
    votes_dict = {vote['poll_info']: vote['vote_count'] for vote in votes_count}
    for nominee in nominees:
        nominee.vote_count = votes_dict.get(nominee.id, 0)
    grouped_nominees = [(sub_category, list(group)) for sub_category, group in groupby(nominees, key=lambda x: x.sub_category)]
    return render(request, 'nominee/nominee_logs.html', {'headline': headline, 'grouped_nominees': grouped_nominees})



@csrf_protect
def google_oauth_vote(request, headline_id):
    headline = get_object_or_404(Headline, id=headline_id)
    request.session['oauth_return_headline'] = str(headline_id)
    return render(request, 'nominee/google_oauth.html', {'headline': headline})



# from allauth.socialaccount.models import SocialAccount

# @csrf_protect
# def nominee_view(request, headline_id):
#     headline = get_object_or_404(Headline, id=headline_id)
    
#     # Check if Google OAuth is required
#     if headline.require_google_auth:
#         if not request.user.is_authenticated:
#             # Store the intended URL to redirect back after login
#             request.session['next_vote_url'] = request.path
#             messages.info(request, 'Please sign in with Google to vote in this poll.')
#             return redirect('google_oauth_vote', headline_id=headline_id)
        
#         # Check if user has Google account linked
#         has_google = SocialAccount.objects.filter(
#             user=request.user,
#             provider='google'
#         ).exists()
        
#         if not has_google:
#             request.session['next_vote_url'] = request.path
#             messages.warning(request, 'This poll requires Google authentication. Please link your Google account.')
#             return redirect('google_oauth_vote', headline_id=headline_id)
    
#     if request.method == 'POST':
#         selected_options = []
#         for key, value in request.POST.items():
#             if key.startswith('option_') and value:
#                 selected_options.append(value)
        
#         if not selected_options:
#             messages.error(request, 'Please select at least one option before submitting your vote.')
#             return redirect('nominee:vote', headline_id=headline_id)
        
#         try:
#             with transaction.atomic():
#                 if request.user.is_authenticated:
#                     existing_votes = vote.objects.filter(user=request.user, headline=headline)
                    
#                     # Check if any existing vote is locked
#                     if existing_votes.filter(is_locked=True).exists():
#                         messages.warning(request, 'Your vote is locked and cannot be changed.')
#                         return redirect('nominee:vote_success')
                    
#                     existing_votes.delete()
#                     for option_id in selected_options:
#                         nominee = get_object_or_404(Poll_information, pk=option_id, headline=headline)
#                         vote.objects.create(user=request.user, poll_info=nominee, headline=headline)
#                 else:
#                     # Anonymous voting only if Google auth not required
#                     if headline.require_google_auth:
#                         messages.error(request, 'Google authentication required to vote.')
#                         return redirect('google_oauth_vote', headline_id=headline_id)
                    
#                     ip_address = get_client_ip(request)
#                     existing_votes = vote.objects.filter(ip_address=ip_address, headline=headline)
                    
#                     if existing_votes.filter(is_locked=True).exists():
#                         messages.warning(request, 'Your vote is locked and cannot be changed.')
#                         return redirect('nominee:vote_success')
                    
#                     if existing_votes.exists():
#                         messages.warning(request, 'You have already voted from this location. Your previous vote has been updated.')
                    
#                     existing_votes.delete()
#                     for option_id in selected_options:
#                         nominee = get_object_or_404(Poll_information, pk=option_id, headline=headline)
#                         vote.objects.create(ip_address=ip_address, poll_info=nominee, headline=headline)
            
#             messages.success(request, 'Your vote has been recorded successfully!')
#             request.session['last_voted_headline'] = str(headline_id)
#             return redirect('nominee:vote_success')
            
#         except Exception as e:
#             messages.error(request, f'An error occurred while recording your vote: {e}')
#             return redirect('nominee:vote', headline_id=headline_id)
    
#     # Check if user has voted and if vote is locked
#     has_voted, is_vote_locked = False, False
    
#     if request.user.is_authenticated:
#         user_votes = vote.objects.filter(user=request.user, headline=headline)
#         has_voted, is_vote_locked = user_votes.exists(), user_votes.filter(is_locked=True).exists()
#     else:
#         ip_address = get_client_ip(request)
#         ip_votes = vote.objects.filter(ip_address=ip_address, headline=headline)
#         has_voted, is_vote_locked = ip_votes.exists(), ip_votes.filter(is_locked=True).exists()
    
#     nominees = Poll_information.objects.filter(headline=headline).only('id', 'sub_category', 'Name', 'headline').order_by('sub_category')
#     grouped_nominees = [(sub_category, list(group)) for sub_category, group in groupby(nominees, key=lambda x: x.sub_category)]
    
#     return render(request, 'nominee/voting_centre.html', {
#         'headline': headline,
#         'grouped_nominees': grouped_nominees,
#         'has_voted': has_voted,
#         'is_vote_locked': is_vote_locked
#     })
