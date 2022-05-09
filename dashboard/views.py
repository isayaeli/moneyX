from django.shortcuts import render
import requests

from .api_calls import call_deposit, deposit_history, get_spot_balance
from .config import *
from .models import AssetBalance
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
    call_deposit(api_key, secret_key, timestamp, pass_phrase, "BTC")
    deposit_history(api_key, secret_key, timestamp, pass_phrase, "USDT")
    # balance = get_spot_balance(api_key, secret_key, timestamp, pass_phrase, "BTC")
    context = {
        "balance":10.798889
    }
    return render(request,'dash/deposits.html', context)


def withdraws(request):
    base_url = 'https://www.okcoin.com'
    request_path = '/api/account/v3/deposit/address?currency=ETH'

    params = {'currency':'ETH'}

    # request path
    request_path = request_path 
    url = base_url + request_path

    # request header and body
    header = get_header(api_key, signature(timestamp, 'GET', request_path,{},secret_key), timestamp, pass_phrase)

    # do request
    response = requests.get(url, headers=header)
    print(response.json())
    context = {
        'balance': response.json()
    }
    return render(request,'dash/withdraws.html', context)