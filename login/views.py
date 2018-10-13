from django.shortcuts import render

# Create your views here.
#views.py
from login.forms import *
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
 
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
        else:
            return render(request, 'registration/register.html', {'form': form})

    else:
        form = RegistrationForm()
        return render(request, 'registration/register.html', {'form': form})
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


class UsernameValidator(View):
    def get(self, request):
        flag = False
        try:
            user = User.objects.get(username = request.GET['user'])
            flag = True
        except ObjectDoesNotExist:
            flag = False
        return HttpResponse(json.dumps({'result': flag}), content_type="application/json")

class EmailValidator(View):
    def get(self, request):
        flag = False
        try:
            user = User.objects.get(email = request.GET['email'])
            flag = True
        except ObjectDoesNotExist:
            flag = False
        return HttpResponse(json.dumps({'result': flag}), content_type="application/json")

@login_required
def home(request):
    return render_to_response(
        'home.html',
        { 'user': request.user }
    )
