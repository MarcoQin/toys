# -*- coding: utf-8 -*-

import re
import random
import requests

from hashlib import md5

APIKEY = ""
APISECRET = ""


class Bilibili(object):

    @classmethod
    def get_live_address(cls, url, index=0):
        roomId = re.findall(b'var ROOMID = (\d+);', requests.get(url).content)[0].decode('ascii')
        url = "platform=android&cid=%s&quality=1&otype=xml&appkey=%s&type=mp4&rnd=%d" % (roomId, APIKEY, random.randint(0, 9999))
        tmp = "%s%s" % (url, APISECRET)
        sign = md5(tmp.encode()).hexdigest()
        print(sign)
        url = "http://live.bilibili.com/api/playurl?%s&sign=%s" % (url, sign)
        print (url)
        return cls.get_address(url, index)

    @classmethod
    def get_address(cls, url, index):
        rt = requests.get(url)
        if rt.status_code == 200:
            rt = rt.content
            print (rt)
            return re.findall(b'<!\\[CDATA\\[(http.*)\\]\\]><\\/.*url>', rt)[index].decode()


if __name__ == "__main__":
    url = "http://live.bilibili.com/1000"
    Bilibili.get_live_address(url)
