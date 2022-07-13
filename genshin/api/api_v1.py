import json
import random
from time import time

import requests
from genshin.models import GenshinUserData
import hashlib

from .api import API

_API_TAKUMI_HOST = 'https://api-takumi.mihoyo.com'
_API_TAKUMI_RECORD_HOST = 'https://api-takumi-record.mihoyo.com'
_SERVER = 'cn_gf01'
_GAME_RECORD_PREFIX = '/game_record/app/genshin/api/'


class APIException(Exception):
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f"code: {self.code}, message: {self.message}"


class API_V1(API):
    def __init__(self, cookie: str):
        self._cookie = cookie

    def index(self, uid: int) -> GenshinUserData:
        url = _API_TAKUMI_RECORD_HOST+_GAME_RECORD_PREFIX + 'index'
        query = f'role_id={uid}&server={_SERVER}'
        url += '?'+query
        headers = getHeaders(query, '', self._cookie)
        rsp = requests.get(url=url, headers=headers)
        js = rsp.json()
        if js['retcode'] != 0:
            raise APIException(js['retcode'], js['message'])
        with open('tmp.json', 'w') as f:
            json.dump(js, f, indent=4)
        return GenshinUserData(**(js["data"]))


def md5(text):
    _md5 = hashlib.md5()
    _md5.update(text.encode())
    return _md5.hexdigest()


def getDs(query: str, body: str):
    n = "xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs"
    t = str(int(time()))
    r = str(random.randint(100001, 999999))
    q = query
    b = body
    ds = md5(f"salt={n}&t={t}&r={r}&b={b}&q={q}")
    return f"{t},{r},{ds}"


def getHeaders(query: str, body: str, cookie: str):
    return {
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://webstatic.mihoyo.com',
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
        'Referer': 'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.mihoyo.hyperion',
        'x-rpc-app_version': '2.26.1',
        'x-rpc-client_type': '5',
        'DS': getDs(query, body),
    }
