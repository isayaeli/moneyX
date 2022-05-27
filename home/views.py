from django.shortcuts import render
from dashboard.config import *
import requests

# Create your views here.
def home(request):
    base_url = 'https://www.okcoin.com'
    request_path = '/api/spot/v3/instruments'


    # request path
    url = base_url + request_path 

    body = {}
    now = datetime.datetime.now()
    timestamp = time.mktime(now.timetuple())

    # request header and body
    header = get_header(api_key, signature(timestamp, 'GET', request_path, body ,secret_key), timestamp, pass_phrase)

    # do request
    response = requests.get(url,  headers=header)
    response = response.json()
    for data in response:
        if data['instrument_id'] == 'ETH-BTC':
            print(data)
    context ={
        'response':response
    }
    return render(request, 'home/index.html',context)