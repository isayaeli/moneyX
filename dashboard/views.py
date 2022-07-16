
import json

from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import requests

from userauth.models import Profile

from .api_calls import call_deposit, call_withdraw, deposit_history, get_trading_info, get_trading_pair, withdraw_history, withd
from .config import *
from .models import AssetBalance, BinaryWithDraw, Deposit, DepositHistory
from django.views.decorators.http import require_http_methods
import websocket
import json
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

        balance_ = Deposit.objects.filter(user=request.user,verify=True)
        count = balance_.count()
        sum_of_user_balance =  sum(balance_.values_list('balance', flat=True))
    

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
    balance = AssetBalance.objects.all().last() #bwallet balance from an api
    balance_ = Deposit.objects.filter(user=request.user,verify=True) #balance tacked fro
    context = {
        'balance': balance,
        "history":history,
        'bal':balance_
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

        if Deposit.objects.filter(currency=currency).exists():
            filt = Deposit.objects.filter(currency=currency).last()
            new_balalance =  filt.balance - int(request.POST['amount'])
            print(new_balalance)
            dp = Deposit.objects.get(id=filt.id)
            dp.balance = new_balalance
            dp.save()
            messages.info(request, f"Your have successful withdrawn {request.POST['amount']} give us a moment we will get to you ASAP")
        else:
            messages.warning(request, "Your do not have any balance for this token Please deposit first")
        withd = call_withdraw(api_key, secret_key,timestamp,pass_phrase, amount,currency,address)
        
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

def swap(request):
    pairs = get_trading_pair(api_key, secret_key, timestamp, pass_phrase)
    ask = get_trading_info()

    print(ask['best_bid'])
    context = {
        'pair':pairs
    }
    return render(request, 'dash/swap.html', context)

def trade(request):
    return render(request, 'dash/trade.html')

@require_http_methods(['GET', 'POST'])
def binary(request):
    token = request.GET.get('token1' or None)
    print(token)
    if token != None:
        profile = Profile.objects.get(user=request.user)
        profile.token = token
        profile.save()
    token = Profile.objects.get(user=request.user)
    # print(token.token)
    res = withd(auth={"authorize": token.token},dataz={"balance": 1})
    # data = json.loads(message)
    data = json.loads(res.mymessage)
    
    # print(data['balance']['balance'])
    # print(data['balance']['currency'])
    # print(data['balance']['loginid'])
    context ={
        'balance': data['balance']['balance']
    }
    return render(request, 'dash/binary.html', context)

def verify(request):
    if request.method == 'POST':
        email = request.POST['email']
        type_ =  request.POST['type']
        response_data = {}
        token = Profile.objects.get(user=request.user)
        res = withd(auth={"authorize": token.token},dataz={"verify_email": email,"type": type_})
        data = json.loads(res.mymessage)
        # print(data['verify_email'])
        response_data['success'] = "code sent successful"
        # response_data['done'] = data['verify_email']
        response_data['message'] = data['error']['message']
        
        return HttpResponse(
            json.dumps(response_data),
            content_type = 'application/json'
        )

    return HttpResponse(
        json.dumps({'Error':"Failded to submit"}),
        content_type = 'application/json'
    )

def binary_agent_withdraw(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        currency = request.POST['currency']
        code = request.POST['code']

        token = Profile.objects.get(user=request.user)
        res = withd(auth={"authorize": token.token},dataz={"paymentagent_withdraw": 1, 'amount':amount,'currency':currency,
                                            'paymentagent_loginid':'CR3724014','verification_code':code})
        data = json.loads(res.mymessage)
        print(data['error']['message'])
        binary = BinaryWithDraw(amount=amount, currency=currency)
        messages.info(request, f"{data['error']['message']}")
        return redirect('binary')

    return JsonResponse()