# -*- coding: utf-8 -*-
from five import *
import datetime, time, random
import logging
from BeautifulSoup import BeautifulSoup
from rk import RClient
from config import *

logger = logging.getLogger()

g_ocr = RClient(rk_user, rk_passwd, rk_app, rk_key)
def identify_image_callback_by_rk(img):
    """识别二维码

    Parameters
    ----------
    img : bytes
        验证码图片二进制数据

    Returns
    -------
    str
        验证码文字
    """
    random_filename = ("./images/%d.png") % (time.time())
    im = readimg(img)
    im.save(random_filename)
    #im.show()
    #return input("please input code: ")
    result = g_ocr.rk_create(img, 3040, 60)
    logger.info(result)
    if not result.has_key('Result') :
        logger.warn("rk error for file:%s", random_filename)
    else:
        img_code = result['Result']
        logger.warn("rk succ for file:%s, code:%s", random_filename, img_code)
        im.close()
        return img_code
    im.close()
    return None

if __name__ == '__main__':
    pass

