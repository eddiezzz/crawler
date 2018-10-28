# -*- coding: utf-8 -*-

import datetime, time, random
from mysql import *
import logging
import wechatsogou
from util import *

logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(filename)s:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger()
db = mysql()
timeutil = TimeUtil(3, 10)

class ProfileSource():
    def gets(self, size = 1000, offset = 0):
        db.clear_stats()
        db.order_sql = " order by updatetime asc"
        db.limit_sql = " limit %d,%d" % (offset, size)
        return db.table("wechat_mp_profile").find(size)

    def update_time(self, wechat_id):
        db.clear_stats()
        db.where_sql = '''wechat_id = "%s" ''' % (wechat_id)
        return db.table("wechat_mp_profile").save({
            'updatetime': time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            })

class ArticleCrawler():
    def __init__(self):
        self.wechat = wechatsogou.WechatSogouAPI(captcha_break_time=3)

    def fetch_mp_articles(self, wechat_id):
        timeutil.sleep()
        res = self.wechat.get_gzh_article_by_history(wechat_id)
        return res

    def save(self, data):
        wechat_id = data['gzh']['wechat_id']
        articles = data['article']
        for article in articles:
            try:
                self._save_one(article, wechat_id)
            except Exception as e:
                logger.warn(e)
                logger.warn(u"save one failed for article:%s", article['title'])

    def _save_one(self, data, wechat_id):
        db.clear_stats()
        db.where_sql = '''fileid = "%s" and send_id="%s" and wechat_id = "%s" ''' % (data['fileid'], data['send_id'], wechat_id)
        found = db.table(u"wechat_article_profile").find(1)
        if found:
            logger.debug("fileid:%s already in db, ignore", data['fileid'])
            return None
        return db.table("wechat_article_profile").add({
                'author': data['author'],
                'content_url': data['content_url'],
                'source_url': data['source_url'],
                'copyright_stat': data['copyright_stat'],
                'cover_url': data['cover'],
                'datetime': time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(data['datetime'])),
                'fileid': data['fileid'],
                'main': data['main'],
                'send_id': data['send_id'],
                'title': data['title'],
                'type': data['type'],
                'abstract': data['abstract'],
                'wechat_id': wechat_id
                })
        
class Runner():
    def __init__(self):
        self.crawler = ArticleCrawler()
        self.source = ProfileSource()
        self.total = 0
        self.succ = 0

    def _handle_task(self, ids):
        succ_ids = []
        for item in ids:
            wechat_id = item['wechat_id'].encode("utf-8")
            try:
                data = self.crawler.fetch_mp_articles(wechat_id)
                if not data:
                    logger.warn(u"wechat_id: %s fetch_mp_articles None", wechat_id)
                    continue
                logger.info("fetch_mp_articles for wechat_id:%s ok", wechat_id)
                #logger.info(data)
                self.crawler.save(data)
                succ_ids.append(wechat_id)
            except Exception as e:
                logger.warn(u"Exception happen:%s", e.message)
                logger.warn(e)
        self.total += len(ids)
        self.succ += len(succ_ids)
        return succ_ids

    def run_one_task(self, size = 10, offset = 0):
        logger.info("in run one_task, size:%d, offset:%d", size, offset)
        ids = self.source.gets(size, offset)
        logger.debug(ids)
        if ids:
            succ_ids = self._handle_task(ids)
            for wechat_id in succ_ids:
                self.source.update_time(wechat_id)
        if (not ids) or (len(ids) < size):
            return False
        return True

    def run(self):
        size = 10
        offset = 0
        while True:
            more = self.run_one_task(size, offset)
            offset += size
            if not more:
                break
            timeutil.sleep()
        logger.info("total:%d succ:%d", self.total, self.succ)

if __name__ == '__main__':
    runner = Runner()
    runner.run()

