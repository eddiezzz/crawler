#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5
from PIL import Image
import sys
sys.path.append('../')
import config

class RClient(object):
    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    #rc = RClient('username', 'password', 'soft_id', 'soft_key')
    #im = open('a.jpg', 'rb').read()
    #print rc.rk_create(im, 3040)
    filename = "/Users/zhengchangshuai/Downloads/z.png"
    print("filename:" + filename)
    image = Image.open(filename).tobytes()
    #image = open(filename, 'rb').read()

    g_ocr = RClient(rk_user, rk_passwd, rk_app, rk_key)
    result = g_ocr.rk_create(image, 3040, 60)
    print(result)
    if not result.has_key('Result') :
        print("rk error")
    else:
        img_code = result['Result']
        print("rk ocr ok")


