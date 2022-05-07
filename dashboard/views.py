from django.shortcuts import render
import requests
from .config import *
# Create your views here.
def index(request):
    return render(request, 'dash/dash.html')


def deposits(request):
    base_url = 'https://www.okcoin.com'
    request_path = '/api/account/v3/withdrawal'

    params = {"amount":"1","fee":"0.0005","destination":"3","currency":"BTC","to_address":"17DKe3kkkkiiiiTvAKKi2vMPbm1Bz3CMKw","chain":"USDT-ERC20"}

    # request path
    request_path = request_path + parse_params_to_str(params)
    url = base_url + request_path 

    body = json.dumps(params)

    # request header and body
    header = get_header(api_key, signature(timestamp, 'POST', request_path, body ,secret_key), timestamp, pass_phrase)

    # do request
    response = requests.post(url, data=body,  headers=header)
    print(response)
    print(response.text)
    print(timestamp)
    return render(request,'dash/deposits.html')


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