from datetime import datetime, date, timedelta
import requests
import json

def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def datetime_now():
    now = datetime.now()
    return now

def time_now():
    now = datetime.now()
    return now.time()

def today():
    today = date.today()
    return today

def send_request(url, data=None, headers=None, type='get'):
    if type == 'get':
        response = requests.get(url, params=data, headers=headers)
        content = json.loads(response.content)
        headers = response.headers
    else:
        response = requests.post(url, json=data, headers=headers)
        content = json.loads(response.content)
        headers = response.headers

    return content, headers

def create_sublists(lst):
    result = []
    i = 0
    while i < len(lst):
        if i + 1 < len(lst):
            result.append([lst[i], lst[i + 1]])
            i += 2
        else:
            result.append([lst[i]])
            i += 1
    return result