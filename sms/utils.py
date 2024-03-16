import json
import requests
from django.conf import settings

def send_sms(message: str, recipients):
    url = settings.SMS_URL
    params = {'uname': 'hakimdr', 'pass': '52b@4ED', 'from': '+985000171', 'to': recipients,
              'msg': f'{message}'}
    response = requests.post(url, data=json.dumps(params))
    return response.status_code
