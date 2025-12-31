from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.views.generic import *
from .forms import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import qrcode
from io import BytesIO
from base64 import b64encode
from django.urls import reverse
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods


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
    nominee_details = Poll_information.objects.filter(headline_id=headline.id).order_by('headline_id')
    return render(request, '../templates/voting/headline_detail.html', {'headline': headline, 'nominee_details': nominee_details})


@login_required
def headline_delete_simple(request, pk):
    if request.method == 'POST':
        headline = get_object_or_404(Headline, pk=pk)
        title = headline.title
        headline.delete()
        messages.success(request, f'"{title}" deleted successfully.')
        return redirect('voting:x6sad_dashboard')
    return redirect('voting:x6sad_dashboard')


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
def poll_info_delete(request, id):
    if request.method == 'POST':
        poll_info = get_object_or_404(Poll_information, id=id)
        headline_id = poll_info.headline.id
        name = poll_info.Name
        poll_info.delete()
        messages.success(request, f'"{name}" deleted successfully.')
        return redirect('voting:headline_detail', pk=headline_id)
    return redirect('voting:x6sad_dashboard')


@login_required
def nominee_detail(request, id):
    poll_info = get_object_or_404(Poll_information, id=id)
    return render(request, '../templates/voting/nominee_detail.html', {'poll_info': poll_info})


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


@login_required
def poll_edit(request, id):
    poll_info = get_object_or_404(Poll_information, id=id)
    if request.method == 'POST':
        form = PollInformationForm(request.POST, request.FILES, instance=poll_info)
        if form.is_valid():
            form.save()
            return redirect('voting:nominee_detail', id=id)
    else:
        form = PollInformationForm(instance=poll_info)
    return render(request, '../templates/voting/poll_edit.html', {'form': form, 'poll_info': poll_info})


@login_required
@require_http_methods(["POST"])
@csrf_protect
def vote_changes(request, pk):
    if request.method == 'POST':
        try:
            headline = get_object_or_404(Headline, pk=pk, creator=request.user)
            data = json.loads(request.body)
            new_state = data.get('allow_vote_changes')
            if new_state is not None:
                headline.allow_vote_changes = new_state
                headline.save()
                return JsonResponse({'status': 'success', 'allow_vote_changes': headline.allow_vote_changes})
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
@require_http_methods(["POST"])
@csrf_protect
def google_auth_requirement(request, pk):
    if request.method == 'POST':
            try:
                headline = get_object_or_404(Headline, pk=pk, creator=request.user)
                data = json.loads(request.body)
                new_value = data.get('require_google_auth', False)
                headline.require_google_auth = new_value
                headline.save()
                return JsonResponse({'success': True, 'require_google_auth': headline.require_google_auth})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=500)