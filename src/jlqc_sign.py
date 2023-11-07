import requests
import time
import hashlib
from os import environ
from util import logger, notify

log = logger.get_logger()


def sign():
    url = 'https://app.geely.com/api/v1/userSign/sign/'
    ts = int(time.time())
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
    cid = 'BLqo2nmmoPgGuJtFDWlUjRI2b1b'
    body = {
        'signDate': formatted_time,
        'ts': str(ts),
        'cId': cid
    }
    token = environ['JLQC_TOKEN']
    x_data_sign = hashlib.md5(f'cId={cid}&signDate={ts}000&ts={ts}0]3K@\'9MK+6Jf'.encode()).hexdigest()
    headers = {
        'origin': 'https://app.geely.com',
        'referer': 'https://app.geely.com/app-h5/sign-in?showTitleBar=0',
        'x-requested-with': 'com.geely.consumer',
        'token': token,
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; M2007J3SC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/96.0.4664.104 Mobile Safari/537.36/android/geelyApp',
        'x-data-sign': x_data_sign,
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
    }
    resp = requests.post(url, headers=headers, json=body).json()
    if resp['code'] == 'success':
        log.info('✅签到成功：' + str(resp))
    else:
        notify.send_notify('吉利汽车签到失败', str(resp))
        log.error('❌签到失败：' + str(resp))


if __name__ == '__main__':
    sign()
