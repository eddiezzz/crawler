# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from utils import *
import config
import datetime, time, random
import logging
from BeautifulSoup import BeautifulSoup

logger = logging.getLogger()

total_failed = 0

g_ocr = RClient(config.rk_user, config.rk_passwd, config.rk_app, config.rk_key)
def identify_weixin_image(img):
    random_filename = ("./images/wexin_%d.png") % (time.time())
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
        logger.info("rk succ for file:%s, code:%s", random_filename, img_code)
        #im.close()
        return img_code
    im.close()
    return None

def identify_sogou_image(img):
    random_filename = ("./images/sogou_%d.png") % (time.time())
    im = readimg(img)
    im.save(random_filename)
    #im.show()
    #return input("please input code: ")
    result = g_ocr.rk_create(img, 3060, 60)
    logger.info(result)
    if not result.has_key('Result') :
        logger.warn("rk error for file:%s", random_filename)
    else:
        img_code = result['Result']
        logger.info("rk succ for file:%s, code:%s", random_filename, img_code)
        im.close()
        return img_code
    im.close()
    return None

def report_error(id):
    pass


if __name__ == '__main__':
    pass

