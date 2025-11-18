
from django.db.models import F
from .models import *
from voting.models import *
from django.shortcuts import get_object_or_404, render
from itertools import groupby
from django.contrib import messages
from django.shortcuts import redirect
from django.db import transaction, IntegrityError


from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction
from itertools import groupby
from .models import Headline, Poll_information, Vote  # Import Vote model
from django.db.models import F

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
            print("Starting transaction...")  # Debug
            with transaction.atomic():
                # Delete any existing votes for this user and headline
                existing_votes = Vote.objects.filter(user=request.user, headline=headline)
                print(f"Existing votes count: {existing_votes.count()}")  # Debug
                existing_votes.delete()

                # Create new votes for selected options
                for option_id in selected_options:
                    nominee = get_object_or_404(Poll_information, pk=option_id, headline=headline)
                    Vote.objects.create(user=request.user, poll_info=nominee, headline=headline)
                    print(f"Created vote for {nominee.Name} (ID: {option_id})")  # Debug
                    #You may want to remove this section as the vote is in another table and it may lead to inconsistency
                    #Poll_information.objects.filter(pk=option_id).update(votes=F('votes') + 1)
                    #nominee.refresh_from_db()
                    #print(f"New vote count for {nominee.Name}: {nominee.votes}")  # Debug

            print("Transaction completed - redirecting to success page")  # Debug
            messages.success(request, 'Your vote has been recorded successfully!')
            return redirect('nominee:vote_success')

        except Exception as e:  # Catch any potential exceptions during vote saving
            print(f"Exception caught: {str(e)}")  # Debug
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