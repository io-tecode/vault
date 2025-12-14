from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.views.generic import *
from .forms import *
from django.contrib.auth.decorators import login_required
import qrcode
from io import BytesIO
from base64 import b64encode
from django.urls import reverse


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
def generate_shareable_link(request, headline_id):
    headline = get_object_or_404(Headline, pk=headline_id)
    try:
        voting_url = reverse('nominee:vote', args=[headline_id])
    except Exception as e:
        print(f"Error reversing URL: {e}")
        voting_url = f'/vote/{headline_id}/'
    shareable_link = request.build_absolute_uri(voting_url)
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4,)
    qr.add_data(shareable_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    qr_code_image = b64encode(buffer.read()).decode('utf-8')
    return render(request, 'voting/shareable_link.html', {'shareable_link': shareable_link, 'qr_code_image': qr_code_image, 'headline': headline})