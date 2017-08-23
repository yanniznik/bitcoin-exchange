import decimal
import json

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

import exchange
from exchanges.bitfinex import Bitfinex
from exchanges.coindesk import CoinDesk

from django.utils.translation import gettext as _

# Create your views here.
from exchange.forms import ProfileForm, UserForm
from exchange.models import Transactions, Wallets, Contacts, Profile

# Fetching current price at server launch to avoid lagging
current_price_usd = Bitfinex().get_current_price()

class WebsiteCommonMixin(generic.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(WebsiteCommonMixin, self).get_context_data(**kwargs)
        try:
            context.update(dict(contact_list = Contacts.objects.filter(friend = User.objects.filter(id=self.request.user.id)).order_by('-created_at')[:], transaction_list = Transactions.objects.filter(walletFrom = Wallets.objects.filter(owner=self.request.user.id)).order_by('-created_at')[:5],wallet = Wallets.objects.get(owner = User.objects.filter(id=self.request.user.id)),template = loader.get_template('exchange/dashboard.html'), current_user = User.objects.get(id=self.request.user.id), current_price_usd = current_price_usd))
            return context
        except:
            return context
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WebsiteCommonMixin, self).dispatch(*args, **kwargs)


class dashboard(WebsiteCommonMixin, TemplateView):
    template_name='exchange/dashboard.html'
    # def get_context_data(self, **kwargs):
    #     context = super(dashboard, self).get_context_data(**kwargs)
    #     context["test"] = "test"
    #     return context

class send(WebsiteCommonMixin, TemplateView):
    template_name='exchange/send.html'

def account(context):
    template = loader.get_template('exchange/account.html')
    return HttpResponse(template.render())

def historicaldata(request):
    if request.method == 'GET':
        data = CoinDesk().get_historical_data_as_dict(start='2017-08-01', end=None)
        return HttpResponse(json.dumps(data))

JSONEncoder_olddefault = json.JSONEncoder.default
def JSONEncoder_newdefault(self, o):
    if isinstance(o, decimal.Decimal): return str(o)
    return JSONEncoder_olddefault(self, o)
json.JSONEncoder.default = JSONEncoder_newdefault

@csrf_exempt
def processing(request):
    if request.method == 'POST':
        data = {}
        try:
            if request.POST['walletTo'] == "stranger":
                walletTo = Wallets.objects.get(address = "1234")
            else:
                walletTo = Wallets.objects.get(address = request.POST['walletTo'])
            walletFrom = Wallets.objects.get(address = request.POST['walletFrom'])
            amount = request.POST['amount']
            description = request.POST['description']
            walletFrom.amount = walletFrom.amount - decimal.Decimal(amount)
            if walletFrom.amount - decimal.Decimal(amount) < 0:  # server-side hacking prevention
                data["code"] = "401"
                data['result'] = 'Not enough money on wallet!'
                return HttpResponse(json.dumps(data), content_type="application/json")
            new_transaction = Transactions(walletFrom = walletFrom, walletTo = walletTo, amount = amount, description = description)
            new_transaction.save()
            walletFrom.save()
            walletTo.amount = walletTo.amount + decimal.Decimal(amount)
            walletTo.save()
            data["code"] = "200"
            data['result'] = 'Successfully sent money'
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Wallets.DoesNotExist:
            data["code"] = "400"
            data['result'] = 'Wallet does not exist in database'
            return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def createcontact(request):
    if request.method == 'POST':
        data = {}
        try:
            friend = User.objects.get(id = request.user.id)
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            wallet = request.POST['wallet']
            new_contact = Contacts(first_name = first_name, last_name = last_name, email = email, friend = friend, wallet = wallet)
            new_contact.save()
            data["code"] = "200"
            data['result'] = 'Successfully saved contact'
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception as e:
            data["code"] = "401"
            data["error"] = str(e.args)
            return HttpResponse(json.dumps(data), content_type="application/json")


    # Do your logic here coz you got data in `get_value`

@csrf_exempt
def checkwallet(request):
    if request.method == 'POST':
        data = {}
        try:
            Wallets.objects.get(address = request.POST['walletTo'])
            data['result'] = 'known'
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Wallets.DoesNotExist:
            data['result'] = 'unknown'
            return HttpResponse(json.dumps(data), content_type="application/json")

class request(WebsiteCommonMixin, TemplateView):
    template_name='exchange/request.html'

def history(request):
    transaction_list = Transactions.objects.order_by('-created_at')[:]
    wallet = Wallets.objects.get(owner = request.user.id)
    template = loader.get_template('exchange/history.html')
    current_user = request.user
    context = {
        "current_user": current_user,
        'transaction_list': transaction_list,
        'wallet': wallet
    }
    return HttpResponse(template.render(context, request))

def contacts(request):
    contact_list = Contacts.objects.order_by('-created_at')[:]
    wallet = Wallets.objects.get(owner = request.user.id)
    template = loader.get_template('exchange/contacts.html')
    current_user = request.user
    wallet_worth = round((current_price_usd * wallet.amount), 2)
    context = {
        "current_user": current_user,
        'contact_list': contact_list,
        'wallet': wallet,
        'current_price_usd': current_price_usd,
        'wallet_worth': wallet_worth,
    }
    return HttpResponse(template.render(context, request))

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