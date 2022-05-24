import json
import requests
from .config import get_header, parse_params_to_str, signature
import time
import datetime
def call_deposit(api_key, secret_key, timestamp, pass_phrase, currency):
    base_url = 'https://www.okcoin.com'
    request_path = '/api/account/v3/deposit/address'

    params = {'currency':currency}

    # request path
    request_path = request_path + parse_params_to_str(params)
    url = base_url + request_path 

    body = {}
    now = datetime.datetime.now()
    timestamp = time.mktime(now.timetuple())

    # request header and body
    header = get_header(api_key, signature(timestamp, 'GET', request_path, body ,secret_key), timestamp, pass_phrase)

    # do request
    response = requests.get(url,  headers=header)
    response = response.json()
    print(response)
    return response


def deposit_history(api_key, secret_key, timestamp, pass_phrase, currency):
    base_url = 'https://www.okcoin.com'
    request_path = '/api/account/v3/deposit/history'

    params = {'currency':currency}

    # request path
    # request_path = request_path + parse_params_to_str(params)
    url = base_url + request_path 

    body = {}
    now = datetime.datetime.now()
    timestamp = time.mktime(now.timetuple())

    # request header and body
    header = get_header(api_key, signature(timestamp, 'GET', request_path, body ,secret_key), timestamp, pass_phrase)

    # do request
    response = requests.get(url,  headers=header)
    print(response.text)
    response = response.json()
    return response



def get_spot_balance(api_key, secret_key, timestamp, pass_phrase, currency):
    base_url = 'https://www.okcoin.com'
    request_path = '/api/spot/v3/accounts'

    params = {'currency':currency}

    # request path
    request_path = request_path + parse_params_to_str(params)
    url = base_url + request_path 

    body = {}
    now = datetime.datetime.now()
    timestamp = time.mktime(now.timetuple())
    # request header and body
    header = get_header(api_key, signature(timestamp, 'GET', request_path, body ,secret_key), timestamp, pass_phrase)

    # do request
    response = requests.get(url,  headers=header)
    print(response)
    res = response.json()
    balance = res[0]['balance']
    print(balance)
    return balance



def call_withdraw(api_key, secret_key, timestamp, pass_phrase, amount, currency, address):
    base_url = 'https://www.okcoin.com'
    request_path = '/api/account/v3/withdrawal'

    params =  {"amount":amount,"fee":"0.0005","destination":"3","currency":currency,"to_address":address,"chain":"USDT-ERC20"}

    # request path
    request_path = request_path 
    url = base_url + request_path
    body = json.dumps(params)
    now = datetime.datetime.now()
    timestamp = time.mktime(now.timetuple())
    # request header and body
    header = get_header(api_key, signature(timestamp, 'POST', request_path,body,secret_key), timestamp, pass_phrase)

    # do request
    response = requests.post(url, data=body, headers=header)
    print(response)
    print(response.json())
    response = response.json()
    return response

def withdraw_history(api_key, secret_key, timestamp, pass_phrase):
    base_url = 'https://www.okcoin.com'
    request_path = '/api/account/v3/withdrawal/history'

    # request_path = request_path + parse_params_to_str(params)
    url = base_url + request_path
    body = {}
    now = datetime.datetime.now()
    timestamp = time.mktime(now.timetuple())

    # request header and body
    header = get_header(api_key, signature(timestamp, 'GET', request_path,body, secret_key), timestamp, pass_phrase)

    # do request
    response = requests.get(url,  headers=header)
    print(response)
    response = response.json()
    print(response)
    return response