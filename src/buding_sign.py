import time
from util import logger, notify
import requests
import re

log = logger.get_logger()
session = requests.session()
session.headers[
    'user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'


def dataenc(ktimes, jqnonce):
    t = ktimes % 10
    if t == 0:
        t = 1
    cs = []
    for c in jqnonce:
        cs.append(chr(ord(c) ^ t))
    return "".join(cs)


def spider():
    url = 'https://www.wjx.cn/vm/QqT9WfU.aspx'
    html = session.get(url).text
    rndnum = re.search(r'var rndnum\s*=\s*"(.+)";', html).group(1)
    jqnonce = re.search(r'var jqnonce\s*=\s*"(.+)";', html).group(1)
    starttime = re.search(r'<\s*input\s+type="hidden"\s+value="(.+)"\s+id="starttime"\s+name="starttime"\s*/>',
                          html).group(1)
    activityId = re.search(r'var activityId\s*=\s*(.+);', html).group(1)
    return {
        'rndnum': rndnum,
        'jqnonce': jqnonce,
        'starttime': starttime,
        'activityId': int(activityId),
    }


# '1,6,14,7,5,0,2,12,9,11,10,13,8,3,4'
def jqParam(activityId, starttime, rndnum):
    _0x4b9009 = rndnum.split('.')[0]
    _0x37348b = abcd2(int(_0x4b9009), 3597397)
    # 14
    _0x307a46 = list(str(_0x37348b))
    # 5
    _0x17071c = int(time.mktime(time.strptime(starttime, '%Y/%m/%d %H:%M:%S')))
    # 0
    _0x12e25a = str(_0x17071c)
    # 2
    if _0x17071c % 10 > 0:
        _0x12e25a = _0x12e25a[::-1]
    activityId = activityId ^ 2130030173
    _0x24bc24 = int(_0x12e25a + '89123')
    # 9
    _0x307a46 = list(str(_0x24bc24) + str(_0x37348b))
    # 11
    _0xd36323 = abcd4(_0x307a46, 'kgESOLJUbB2fCteoQdYmXvF8j9IZs3K0i6w75VcDnG14WAyaxNqPuRlpTHMrhz')
    # 10
    _0xc23193 = _0x24bc24 + _0x37348b + activityId
    # 13
    jqParam = abcd3(_0xc23193, _0xd36323)
    jqParam = abcd5(jqParam)
    return jqParam


# 4 9 5 2 0 3 8 7 6 1
def abcd2(_0x5d3f51, _0x2da958):
    _0x17fe67 = 2147483648
    _0x330f76 = 2147483647
    _0x33045d = ~~(int(_0x2da958 / _0x17fe67))  # 0
    _0x8c2ab2 = ~~(int(_0x5d3f51 / _0x17fe67))
    _0xa5b0b1 = _0x5d3f51 & _0x330f76
    _0x352369 = _0x2da958 & _0x330f76
    _0x3f97b8 = _0x8c2ab2 ^ _0x33045d
    _0x4307f8 = _0xa5b0b1 ^ _0x352369
    return _0x3f97b8 * _0x17fe67 + _0x4307f8


def abcd3(a: int, s):
    if a < 62:
        return s[a]
    x = a % 62
    y = int(a / 62)
    return abcd3(y, s) + s[x]


# 5|4|3|1|2|0
def abcd4(_0x2d1e33, _0x4ccbfe):
    _0x39c799 = list(_0x4ccbfe)
    _0x368c45 = len(_0x4ccbfe)
    for i in range(len(_0x2d1e33)):
        _0x1e44d9 = int(_0x2d1e33[i])
        _0x172ebc = _0x39c799[_0x1e44d9]
        _0x939174 = _0x39c799[_0x368c45 - 1 - _0x1e44d9]
        _0x39c799[_0x1e44d9] = _0x939174
        _0x39c799[_0x368c45 - 0x1 - _0x1e44d9] = _0x172ebc

    _0x4ccbfe = _0x39c799
    return ''.join(_0x4ccbfe)


# 7|1|9|6|2|5|3|8|4|0
def abcd5(_0x30fc22):
    _0x416034 = 0
    _0x39f6f7 = _0x30fc22
    for c in _0x39f6f7:
        _0x416034 += ord(c)
    _0x33f508 = len(_0x30fc22)
    _0x51436b = _0x416034 % _0x33f508
    _0xd1d5ab = []
    for i in range(_0x51436b, _0x33f508):
        _0xd1d5ab.append(_0x39f6f7[i])
    for i in range(0, _0x51436b):
        _0xd1d5ab.append(_0x39f6f7[i])
    return ''.join(_0xd1d5ab)


def sign():
    info = spider()
    log.info(str(info))
    time.sleep(20)
    url = 'https://www.wjx.cn/joinnew/processjq.ashx'
    activityId = info['activityId']
    ktimes = 23
    starttime = info['starttime']
    rndnum = info['rndnum']
    headers = {
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://www.wjx.cn',
        'Referer': 'https://www.wjx.cn/vm/QqT9WfU.aspx',
    }
    params = {
        'shortid': 'QqT9WfU',
        'starttime': starttime,
        'cst': str(int(time.time() * 1000)),
        'submittype': '1',
        'ktimes': str(ktimes),
        'hlv': '1',
        'rn': info['rndnum'],
        'jqpram': jqParam(activityId, starttime, rndnum),
        'nw': '1',
        'jwt': '16',
        'jpm': '87',
        't': str(int(time.time() * 1000)),
        'jqnonce': info['jqnonce'],
        'jqsign': dataenc(ktimes, info['jqnonce']),
    }
    body = {
        'submitdata': '1$1!布丁47400822^2!15858203675'
    }
    text = session.post(url, data=body, params=params, headers=headers).text
    log.info('submit resp: ' + text)
    if text[0:2] != '10':
        notify.send_notify('布丁签到失败', text)


if __name__ == '__main__':
    sign()
