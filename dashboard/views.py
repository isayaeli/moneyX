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
        now = datetime.datetime.now()
        timestamp = time.mktime(now.timetuple())

        # request header and body
        header = get_header(api_key, signature(timestamp, 'GET', request_path, body ,secret_key), timestamp, pass_phrase)

        # do request
        response = requests.get(url, data=body, headers=header)
        print(response)
        response = response.json()
        api_balance =response['balance']
        print(api_balance)
        dbbalance = AssetBalance(balance=api_balance)
        balance = AssetBalance.objects.all().last()
        if api_balance != balance:
            dbbalance.save()
            del_balance = AssetBalance.objects.all()[:1]
            for data in del_balance:
                data.delete()

        
    except:
        balance = AssetBalance.objects.all().last()
        print(f"this is from db {balance}")
    

    context = {
        'data':balance
    }
    return render(request, 'dash/dash.html', context)


def deposits(request):

    saved_history = DepositHistory.objects.values('history')
    history =deposit_history(api_key, secret_key, timestamp, pass_phrase)
    save_hist = DepositHistory(history=history)


    saved_history = saved_history[0]['history']
    for data in history:
        for saved_data in saved_history:
            saved = saved_data['timestamp']
        from_api = data['timestamp']
        
    if saved != from_api or saved == None:
        save_hist.save()


    history = DepositHistory.objects.values('history')

    balance = AssetBalance.objects.all().last()
    context = {
        "balance":balance,
        "history":history
    }
    return render(request,'dash/deposits.html', context)


def deposit_address(request):
    if request.method == 'POST':
      
        print(timestamp)
        currency = request.POST['currency']
        deposit_address = call_deposit(api_key, secret_key, timestamp, pass_phrase, currency)
    context = {
        'address':deposit_address
    }
    return render(request, 'dash/deposit_address.html', context )



def withdraws(request):
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
        print(request.POST)
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        address = request.POST.get('address')
    withd = call_withdraw(api_key, secret_key,timestamp,pass_phrase, amount,currency,address)
    context = {
        'data':withd['error_message']
    }
    return render(request, 'dash/finish_withdraw.html',context)