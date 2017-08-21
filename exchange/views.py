from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from django.utils.translation import gettext as _

# Create your views here.
from exchange.forms import ProfileForm, UserForm
from exchange.models import Transactions, Wallets

@login_required(login_url='/login/')
def dashboard(request):
    transaction_list = Transactions.objects.order_by('-created_at')[:]
    wallet = Wallets.objects.get(owner = request.user.id)
    template = loader.get_template('exchange/dashboard.html')
    current_user = request.user
    context = {
        "current_user": current_user,
        'transaction_list': transaction_list,
        'wallet': wallet
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='/login/')
def send(request):
    template = loader.get_template('exchange/send.html')
    context = {}
    return HttpResponse(template.render(context, request))

def account(context):
    template = loader.get_template('exchange/account.html')
    return HttpResponse(template.render())

def history(context):
    template = loader.get_template('exchange/history.html')
    return HttpResponse(template.render())

def contacts(context):
    template = loader.get_template('exchange/contacts.html')
    return HttpResponse(template.render())

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'exchange/signup.html', {'form': form})

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        print(profile_form)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'exchange/account.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })