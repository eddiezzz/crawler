# -*- coding: utf-8 -*-

from wechatsogou.tools import *
from wechatsogou import *
from PIL import Image
import datetime
import time
import sys,locale
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.info("start")

wechats = WechatSogouApi()

mysql = mysql('add_mp_list')
add_list = mysql.find(0)
succ_count = 0

for add_item in add_list :
    try:
        logger.info(add_item)
        if add_item['wx_hao']:
            logger.info("add by wx_hao")
            mysql.where_sql = "wx_hao ='" + add_item['wx_hao'] + "'"
            mp_data = mysql.table('mp_info').find(1)
            if not mp_data :
                wechat_info = wechats.get_gzh_info(add_item['wx_hao'])
                time.sleep(1)
                logger.info(wechat_info)
                if(wechat_info != ""):
                    mysql.table('mp_info').add({'name':wechat_info['name'],
                                                'wx_hao':wechat_info['wechatid'],
                                                'company':wechat_info['renzhen'],
                                                'description':wechat_info['jieshao'],
                                                'logo_url':wechat_info['img'],
                                                'qr_url': wechat_info['qrcode'],
                                                'wz_url': wechat_info['url'],
                                                'last_qunfa_id': 0,
                                                'create_time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))})
                else:
                    logger.info(u"wechat info for id:" + add_item['wx_hao'] + " error")
            else:
                logger.info(u"已经存在的公众号")
        elif add_item['name']:
            logger.info("add by name")
            wechat_infos = wechats.search_gzh_info(add_item['name'].encode('utf8'))
            time.sleep(1)
            logger.info(wechat_infos)
            cnt = 3
            for wx_item in wechat_infos :
                cnt = cnt - 1
                if cnt <= 0:
                    logger.info("too many wx_hao match the name, just take top3")
                    break
                
                logger.info(wx_item['name'])
                mysql.where_sql = "wx_hao ='" + wx_item['wechatid'] + "'"
                logger.info(mysql.where_sql)
                mp_data = mysql.table('mp_info').find(1)
                if not mp_data :
                    logger.info(wx_item['name'].decode("utf-8"))
                    mysql.table('mp_info').add({ 'name':wx_item['name'],
                                'wx_hao':wx_item['wechatid'],
                                'company':wx_item['renzhen'],
                                'description':wx_item['jieshao'],
                                'logo_url':wx_item['img'],
                                'qr_url': wx_item['qrcode'],
                                'wz_url': wx_item['url'],
                                'last_qunfa_id': 0,
                                'create_time':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))})
                else:
                    logger.info(u"已经存在的公众号")
                
        #删除已添加项
        mysql.table('add_mp_list').where({'_id':add_item['_id']}).delete()
    except Exception, e:
        #logger.info(u"出错，继续" + e.message + " for wx_hao:" + add_item['_id'])
        logger.info(u"出错，继续" + e.message )
        continue

logger.info("all process over")

    

