import hmac
import base64 as Base64
import time
from datetime import datetime
import datetime
from django.conf import settings
from django.utils.timezone import get_current_timezone

CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'
APPLICATION_JSON = 'application/json'

#geting time stamp
# def get_time():
#     urltime= 'https://www.okcoin.com/api/general/v3/time'
#     response=requests.get(urltime)
#     time=response.json()
#     time=time['iso']
#     return time

# signature
def signature(timestamp, method, request_path, body, secret_key):
    if str(body) == '{}' or str(body) == 'None':
        body = ''
    message = str(timestamp) + str.upper(method) + request_path + str(body)
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return Base64.b64encode(d)


# set request header
def get_header(api_key, sign, timestamp, passphrase):
    header = dict()
    header[CONTENT_TYPE] = APPLICATION_JSON
    header[OK_ACCESS_KEY] = api_key
    header[OK_ACCESS_SIGN] = sign
    header[OK_ACCESS_TIMESTAMP] = str(timestamp)
    header[OK_ACCESS_PASSPHRASE] = passphrase
    return header


def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        url = url + str(key) + '=' + str(value) + '&'

    return url[0:-1]


api_key = settings.OK_API_KEY
secret_key = settings.OK_SECRETE_KEY
# timestamp = 2022-06-09T19:17:47.759Z
# timestamp = f"{datetime.datetime.utcnow().isoformat()[:-3]}Z"
# timestamp = get_time()
now = datetime.datetime.now()
timestamp = time.mktime(now.timetuple())
print(timestamp)
pass_phrase = settings.PASS_PHRASE