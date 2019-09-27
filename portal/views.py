from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import SubmitForm

# Create your views here.
@login_required(login_url='/auth/login/')
def home(request):
    user = request.user
    if not hasattr(user, 'team'):
        return HttpResponseRedirect(reverse('logout'))
    team = user.team
    
    if team.problem == '':
        return HttpResponseRedirect(reverse('portal:error'))

    show_msg = False

    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES, instance=team)

        if form.is_valid():        
           form.save()
           show_msg = True
    

    form = SubmitForm(instance=team)

    context = {
        'form': form,
        'show_msg': show_msg,
    }

    return render(request, 'portal/home.html', context)

@login_required(login_url='/auth/login/')
def error(request):
    return HttpResponse('Your profile is improperly configured. Contact a member of our team now.')
