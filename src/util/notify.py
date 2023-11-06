import requests
from . import logger

log = logger.get_logger()


def send_notify(title, content):
    url = 'https://xizhi.qqoq.net/XZ64b2e3f239e7b355cb82f34cf19dd291.send'
    body = {
        'title': title,
        'content': content
    }
    log.info('send notify start: ' + str(body))
    # {"code":200,"msg":"推送成功"}
    resp = requests.post(url, data=body).json()
    if resp['code'] != 200:
        log.error('send notify fail,resp=' + str(resp))
