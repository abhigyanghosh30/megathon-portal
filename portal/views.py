from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import SubmitForm

# Create your views here.
@login_required(login_url='/auth/login/')
def home(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user
            if not hasattr(user, 'team'):
                return HttpResponseRedirect(reverse('django.contrib.auth.views.logout'))
            
            team = user.team

            team.presentation = request.FILES['presentation']
            team.submission = form.cleaned_data['submission']

            team.save()
    
    else:
        form = SubmitForm()

    context = {
        'form': form,
    }

    return render(request, 'portal/home.html', context)

