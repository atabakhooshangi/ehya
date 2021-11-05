import json
import requests


def send_sms(message: str, recipients):
    url = 'http://185.4.28.100/class/sms/restful/sendSms_OneToMany.php'
    params = {'uname': 'hakimdr', 'pass': '52b@4ED', 'from': '+985000171', 'to': recipients,
              'msg': f'{message}'}
    response = requests.post(url, data=json.dumps(params))
    return response.status_code
