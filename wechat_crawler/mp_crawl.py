# -*- coding: utf-8 -*-

import datetime, time, random
from mysql import *
import logging
import wechatsogou
from util import *

logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(filename)s:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger()
timeutil = TimeUtil(3, 5)
db = mysql()

class WechatMpCrawler():
    def __init__(self):
        self.wechat = wechatsogou.WechatSogouAPI(captcha_break_time=3)

    def get_profile(self, wechat_id):
        db.where_sql = '''wechat_id = "%s" or wechat_name = "%s" ''' % (wechat_id, wechat_id)
        return db.table("wechat_mp_profile").find(1)

    def fetch(self, wechat_id):
        timeutil.sleep()
        logger.info("search for wechat_id:%s", wechat_id)
        return self.wechat.get_gzh_info(wechat_id)

    def save(self, data):
        db.table("wechat_mp_profile").add({
            'wechat_name': data['wechat_name'],
            'wechat_id': data['wechat_id'],
            'headimage': data['headimage'],
            'qrcode': data['qrcode'],
            'introduction': data['introduction'],
            'authentication': data['authentication'],
            'profile_url': data['profile_url'],
            'post_perm': data['post_perm'],
            'view_perm': data['view_perm'],
            'updatetime': time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            })
        
class CrawlSource():
    def gets(self, size = 10):
        return db.table("wechat_mp_crawl").find(size)
        
    def delete(self, wechat_id):
        res = db.table("wechat_mp_crawl").where({'wechat_id':wechat_id}).delete()
        logger.debug(res)

class Runner():
    def __init__(self):
        self.crawler = WechatMpCrawler()
        self.source = CrawlSource()
        self.total = 0
        self.succ = 0

    def handle_task(self, items):
        succ_ids = []
        for item in items:
            wechat_id = item['wechat_id']
            try:
                if wechat_id  is None or wechat_id == "":
                    wechat_id = item['wechat_name'].encode('utf8')
                profile = self.crawler.get_profile(wechat_id)
                if profile:
                    succ_ids.append(profile['wechat_id'])
                    continue
                data = self.crawler.fetch(wechat_id)
                if data is None:
                    logger.warn(u"wechat_id: %s crawl is None", wechat_id)
                    continue
                logger.info(u"fetch for:%s, name:%s", wechat_id, data["wechat_name"].encode('utf8'))
                self.crawler.save(data)
                succ_ids.append(data['wechat_id'])
            except Exception as e:
                logger.warn(u"Exception happen:%s", e.message)
                logger.warn(e)
        self.total += len(items)
        self.succ += len(succ_ids)
        return succ_ids

    def run_one_task(self, task_size = 10):
        logger.info("in run one_task, size:%d", task_size)
        items = self.source.gets(task_size)
        logger.info(items)
        if not items:
            return False
        succ_ids = self.handle_task(items)
        for wechat_id in succ_ids:
            self.source.delete(wechat_id)
            logger.info(u"wechat_id:%s process ok, remove from source", wechat_id)
        return True

    def run(self):
        while True:
            more = self.run_one_task(10)
            if not more:
                break
            timeutil.sleep()
        logger.info("total:%d succ:%d", self.total, self.succ)

if __name__ == '__main__':
    runner = Runner()
    runner.run()

