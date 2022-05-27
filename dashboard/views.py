import json
from locale import currency

from django.contrib import messages
from django.shortcuts import redirect, render
import requests

from .api_calls import call_deposit, call_withdraw, deposit_history, get_spot_balance, withdraw_history
from .config import *
from .models import AssetBalance, Deposit, DepositHistory
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
        
        balance_ = Deposit.objects.filter(user=request.user,verify=True)
        count = balance_.count()
        sum_of_user_balance =  sum(balance_.values_list('balance', flat=True))

        
    except:
        balance = AssetBalance.objects.all().last()
        print(f"this is from db {balance}")
    

    context = {
        'data':balance, #balnce from okcoin api
        'sum':sum_of_user_balance,
        'count':count
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

    balance_ = Deposit.objects.filter(user=request.user,verify=True)

    sum_of_user_balance =  sum(balance_.values_list('balance', flat=True))
    print(sum_of_user_balance)
  
    balance = AssetBalance.objects.all().last()
    context = {
        "balance":balance,
        "history":history,
        'dp':sum_of_user_balance,
        'bal':balance_
    }
    return render(request,'dash/deposits.html', context)


def deposit_address(request):
    if request.method == 'POST':
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




def track_deposit(request):
    deposit =  Deposit()
    if request.method == 'POST':
        currency = request.POST['currency']
        if Deposit.objects.filter(currency=currency).exists():
            filt = Deposit.objects.filter(currency=currency).last()
            new_balalance = int(request.POST['balance']) + filt.balance
            print(new_balalance)
            dp = Deposit.objects.get(id=filt.id)
            dp.balance = new_balalance
            dp.save()
            messages.info(request, "Your  Deposit Information has been Updated please wait for confirmation to update your balance")
        else:
            deposit.user = request.user
            deposit.balance =request.POST['balance']
            deposit.address = request.POST['address']
            deposit.chain = request.POST['chain']
            deposit.currency = request.POST['currency']
            deposit.save()
            messages.success(request, "Your New Deposit Information has been submited please wait for confirmation to update your balance")
    return redirect('deposits')