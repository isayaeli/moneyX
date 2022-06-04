
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


def deposit_history(api_key, secret_key, timestamp, pass_phrase):
    base_url = 'https://www.okcoin.com'
    request_path = '/api/account/v3/deposit/history'


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
    print(response)
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


def get_trading_pair(api_key, secret_key, timestamp, pass_phrase):
    base_url = 'https://www.okcoin.com'
    request_path = '/api/spot/v3/instruments'

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
    # print(response)
    return response






#==============================================================binary api calls=============================================================================
import websocket
import json
import _thread as thread


class WithD:
    def __init__(self, auth, dataz):
        self.dataz = dataz
        self.auth = auth
        
        def on_open(ws):
            json_data = json.dumps(auth)
            ws.send(json_data)

        def on_message(ws, message):
            data = json.loads(message)
            # print('Data: %s' % message) # Uncomment this line to see all response data.
            self.mymessage = message
            if 'error' in data.keys():
                print('Error Happened: %s' % message)
                # With Websockets we can not control the order things are processed in so we need
                # to ensure that we have received a response to authorize before we continue.
            elif data["msg_type"] == 'authorize':
                print("Authorized OK, so now buy Contract")
                json_data1 = json.dumps(dataz)
                # ws.send(json_data1)
                def run(*args):
                    for i in range(1):
                        time.sleep(1)
                        ws.send(json_data1)
                    time.sleep(1)
                    ws.close()
                thread.start_new_thread(run,())
            # print('ticks update: %s' % message)
            # mymessage = message
           
            # return mymessage
            
        
            
    

        apiUrl = "wss://ws.binaryws.com/websockets/v3?app_id=31700"
        ws = websocket.WebSocketApp(apiUrl, on_message = on_message, on_open = on_open)
        ws.run_forever()
    

withd = WithD



