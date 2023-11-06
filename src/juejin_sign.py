import requests
from os import environ
from util import logger, notify

log = logger.get_logger()


def sign():
    url = 'https://api.juejin.cn/growth_api/v1/check_in?aid=2608&uuid=7162434001180722719&spider=0&_signature=_02B4Z6wo00101mDk8UQAAIDD669qpZdPk35g4PXAAPvFpb0nU-..a8U.k5YxPnnYtbg8eaq5DJJIjJAjDB03OFkjn2c.kGMPYLS0GDKY7j4off.p3QqaRed5aRcnetb6yO4bynyObTzJeO3p3a'
    cookie = '' if environ['JUEJIN_COOKIE'] is None else environ['JUEJIN_COOKIE']
    headers = {
        'cookie': environ['JUEJIN_COOKIE'],
        'origin': 'https://juejin.cn',
        'referer': 'https://juejin.cn/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    # {"err_no":0,"err_msg":"success","resp":{"incr_point":100,"sum_point":571}}
    resp = requests.post(url, headers=headers, json={}).json()
    log.info('juejin sign resp resp: ' + str(resp))
    if resp['err_no'] != 0:
        log.error('juejin sign fail, resp: ' + str(resp))
        notify.send_notify('掘金签到失败', str(resp))


if __name__ == '__main__':
    sign()
