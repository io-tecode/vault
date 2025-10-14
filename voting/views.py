from urllib import request
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.views.generic import *
from .forms import *


def logboard_view(request):
    headlines = Headline.objects.all().order_by('-creation_date')
    context = {'headlines': headlines}
    return render(request, '../templates/plate/logboard.html', context)


def dashboard_view(request):
    return render(request, '../templates/plate/dashboard.html')


def headline_view(request):
    if request.method == 'POST':
        form = HeadlineForm(request.POST, request.FILES)
        if form.is_valid():
            headline = form.save(commit=False)
            # headline.creation_date = timezone.now().date()
            headline.save()
            return redirect('voting:x6sad_dashboard')
            # return render(request, '../templates/plate/dashboard.html')  # Refix: structuring the page a proper layout.
    else:
        form = HeadlineForm()
    return render(request, '../templates/voting/headline_form.html', {'form': form})


def poll_info_view(request):
    if request.method == 'POST':
        form = PollInformationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('voting:x6sad_dashboard')
            # return render(request, '../templates/plate/dashboard.html')  # Refix: structuring the page a proper layout.
    else:
        form = PollInformationForm()
    return render(request, '../templates/voting/pollinfo_form.html', {'form': form})


# def delete_upload_file(request, pk):
#     user = CustomUser.objects.get(pk=request.user.id)
#     if user.is_superuser:
#         file = FileModels.objects.get(pk=pk)
#         file.delete()
#         file_path = os.path.join(settings.MEDIA_ROOT, str(file.file))
#         if os.path.exists(file_path):
#             os.remove(file_path)
#         return redirect('filesystem:upload_list')
#     else:
#         return HttpResponseForbidden('<h1>You are not authorised to view this page</h1>')


class poll_detail_view(DetailView):
    model = Poll
    template_name = 'voting/poll_detail.html'
    context_object_name = 'poll_detail'


def poll_edit_view(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if request.method == 'POST':
        form = PollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            return redirect('poll_detail', pk=poll.pk)  # Redirect to poll detail view
    else:
        form = PollForm(instance=poll)
    return render(request, 'voting/poll_edit.html', {'form': form, 'poll': poll})


def poll_delete_view(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    
    if request.method == 'POST':
        poll.delete()
        return redirect('voting:x6sad_dashboard')  # Redirect to dashboard or another appropriate page
    return render(request, 'voting/poll_confirm_delete.html', {'poll': poll})