from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.views.generic import *
from .forms import *
from django.contrib.auth.decorators import login_required
import qrcode
from io import BytesIO
from base64 import b64encode
from django.urls import reverse


# @login_required
# def logboard_view(request):
#     headlines = Headline.objects.all().order_by('-creation_date')
#     context = {'headlines': headlines}
#     return render(request, '../templates/plate/logboard.html', context)


@login_required
def dashboard_view(request):
    account_user = request.user
    headlines = Headline.objects.filter(creator=account_user).order_by('-creation_date')
    return render(request, '../templates/plate/dashboard.html', {'account_user': account_user, 'headlines': headlines})


@login_required
def headline_view(request):
    if request.method == 'POST':
        form = HeadlineForm(request.POST, request.FILES)
        if form.is_valid():
            headline = form.save(commit=False)
            headline.creator = request.user
            headline.save()
            return redirect('voting:x6sad_dashboard')
    else:
        form = HeadlineForm()
    return render(request, '../templates/voting/headline_form.html', {'form': form})


@login_required
def headline_detail(request, pk):
    headline = get_object_or_404(Headline, pk=pk)
    votee_details = Poll_information.objects.filter(headline_id=headline.id).order_by('headline_id')
    return render(request, '../templates/voting/headline_detail.html', {'headline': headline, 'votee_details': votee_details})


@login_required
def poll_info_view(request):
    headline_id = request.GET.get('headline_id')
    headline = get_object_or_404(Headline, pk=headline_id)
    if request.method == 'POST':
        form = PollInformationForm(request.POST, request.FILES)
        if form.is_valid():
            poll_info = form.save(commit=False)
            poll_info.headline = headline
            poll_info.save()
            return redirect('voting:headline_detail', pk=headline_id)
    else:
        form = PollInformationForm()
    return render(request, '../templates/voting/pollinfo_form.html', {'form': form, 'headline_id': headline_id})


@login_required
def votee_detail(request, id):
    poll_info = get_object_or_404(Poll_information, id=id)
    return render(request, '../templates/voting/votee_detail.html', {'poll_info': poll_info})


@login_required
class poll_detail_view(DetailView):
    model = Poll
    template_name = 'voting/poll_detail.html'
    context_object_name = 'poll_detail'


@login_required
def poll_edit_view(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if request.method == 'POST':
        form = PollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            return redirect('poll_detail', pk=poll.pk)
    else:
        form = PollForm(instance=poll)
    return render(request, 'voting/poll_edit.html', {'form': form, 'poll': poll})


@login_required
def poll_delete_view(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    
    if request.method == 'POST':
        poll.delete()
        return redirect('voting:x6sad_dashboard') 
    return render(request, 'voting/poll_confirm_delete.html', {'poll': poll})


def generate_shareable_link(request, headline_id):
    headline = get_object_or_404(Headline, pk=headline_id)
    voting_url = reverse('voting:vote', args=[headline_id])
    shareable_link = request.build_absolute_uri(voting_url)
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4,)
    qr.add_data(shareable_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    qr_code_image = b64encode(buffer.read()).decode('utf-8')
    return render(request, 'voting/shareable_link.html', {'shareable_link': shareable_link, 'qr_code_image': qr_code_image})


def Nominee_view(request, headline_id):
    headline = get_object_or_404(Headline, pk=headline_id)
    return render(request, 'voting/vote_centre.html', {'headline': headline})