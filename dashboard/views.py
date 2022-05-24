import json
from django.shortcuts import redirect, render
import requests

from .api_calls import call_deposit, call_withdraw, deposit_history, get_spot_balance, withdraw_history
from .config import *
from .models import AssetBalance, DepositHistory
# Create your views here.
def index(request):
    try:
        
        base_url = 'https://www.okcoin.com'
        request_path = '/api/account/v3/asset-valuation'
        params = {'valuation_currency': 'USD'}

        # request path
        request_path = request_path + parse_params_to_str(params)
        url = base_url + request_path 
        
        #body params
        body = json.dumps(params)

        # request header and body
        header = get_header(api_key, signature(timestamp, 'GET', request_path, body ,secret_key), timestamp, pass_phrase)

        # do request
        response = requests.get(url, data=body, headers=header)
        print(response)
        response = response.json()
        balance =response['balance']
        print(balance)
        dbbalance = AssetBalance(balance=balance)
        dbbalance.save()
    except:
        balance = AssetBalance.objects.all().last()
        print(f"this is from db {balance}")
    

    context = {
        'data':balance
    }
    return render(request, 'dash/dash.html', context)


def deposits(request):
    now = datetime.datetime.now()
    timestamp = time.mktime(now.timetuple())
    if request.method == 'POST':
        
        try:
            currency = request.POST['currency']
            history =deposit_history(api_key, secret_key, timestamp, pass_phrase, currency)
            hist = DepositHistory(history=history)
            hist.save()
        except:
            history = DepositHistory.objects.values('history')
            # print(all_.amount)
        context = {
            "balance":10.798889,
            "history":history
        }
        return render(request,'dash/deposits.html', context)
    else:
        history =deposit_history(api_key, secret_key, timestamp, pass_phrase, 'BTC')
        hist = DepositHistory(history=history)
        hist.save()
        history = DepositHistory.objects.values('history')
        # print(all_)
        # balance = get_spot_balance(api_key, secret_key, timestamp, pass_phrase, "BTC")
        balance = AssetBalance.objects.all().last()
        context = {
            "balance":balance,
            "history":history
        }
        return render(request,'dash/deposits.html', context)


def deposit_address(request):
    if request.method == 'POST':
        now = datetime.datetime.now()
        timestamp = time.mktime(now.timetuple())
        print(timestamp)
        currency = request.POST['currency']
        deposit_address = call_deposit(api_key, secret_key, timestamp, pass_phrase, currency)
    context = {
        'address':deposit_address
    }
    return render(request, 'dash/deposit_address.html', context )



def withdraws(request):
    now = datetime.datetime.now()
    timestamp = time.mktime(now.timetuple())
    history = withdraw_history(api_key, secret_key, timestamp, pass_phrase)
    balance = AssetBalance.objects.all().last()
    context = {
        'balance': balance,
        "history":history
    }
    return render(request,'dash/withdraws.html', context)


def withdraw_address(request):
    if request.method == 'POST':
        currency = request.POST.get('currency')
    context = {
    
        "currency":currency
    }
    return render(request,'dash/withdraw_address.html', context)


def finish_withdraw(request):
    if request.method == 'POST':
        now = datetime.datetime.now()
        timestamp = time.mktime(now.timetuple())
        print(request.POST)
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        address = request.POST.get('address')
    withd = call_withdraw(api_key, secret_key,timestamp,pass_phrase, amount,currency,address)
    context = {
        'data':withd['error_message']
    }
    return render(request, 'dash/finish_withdraw.html',context)