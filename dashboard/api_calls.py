import requests
from .config import get_header, parse_params_to_str, signature
def call_deposit(api_key, secret_key, timestamp, pass_phrase, currency):
    base_url = 'https://www.okcoin.com'
    request_path = '/api/account/v3/deposit/address'

    params = {'currency':currency}

    # request path
    request_path = request_path + parse_params_to_str(params)
    url = base_url + request_path 

    body = {}

    # request header and body
    header = get_header(api_key, signature(timestamp, 'GET', request_path, body ,secret_key), timestamp, pass_phrase)

    # do request
    response = requests.get(url,  headers=header)
    # print(response.text)
    return response.text


def deposit_history(api_key, secret_key, timestamp, pass_phrase, currency):
    base_url = 'https://www.okcoin.com'
    request_path = '/api/account/v3/deposit/history'

    params = {'currency':currency}

    # request path
    # request_path = request_path + parse_params_to_str(params)
    url = base_url + request_path 

    body = {}

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

    # request header and body
    header = get_header(api_key, signature(timestamp, 'GET', request_path, body ,secret_key), timestamp, pass_phrase)

    # do request
    response = requests.get(url,  headers=header)
    print(response)
    res = response.json()
    balance = res[0]['balance']
    print(balance)
    return balance