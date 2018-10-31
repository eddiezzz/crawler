# -*- coding: utf-8 -*-
from five import *
import datetime, time, random
from mysql import *
import logging
import wechatsogou
from util import *
from urllib2 import Request, urlopen
import hash
from BeautifulSoup import BeautifulSoup
from rk import RClient
from config import *

logging.basicConfig(level=logging.INFO, format='[%(asctime)s - %(filename)s:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger()
db = mysql()
timeutil = TimeUtil(3, 10)

new_articles = 0

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
 
def get_html(url):
    req = Request(url)
    req.add_header('Accept-Encoding', 'utf-8')
    req.add_header('User-agent', 'Mozilla/5.0')
    res = urlopen(req).read()
    return res


def format_html(html):
    soup = BeautifulSoup(html)
    for s in soup('script'):
        s.extract()
    return soup.__str__()

def gen_article_id(content_url):
    #return mmh3.hash128(content_url)
    return hash.murmur64(content_url)

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
        self.wechat = wechatsogou.WechatSogouAPI(captcha_break_time=1)

    def fetch_mp_articles(self, wechat_id):
        timeutil.sleep()
        res = self.wechat.get_gzh_article_by_history(wechat_id, identify_image_callback_sogou=identify_image_callback_by_rk, identify_image_callback_weixin=identify_image_callback_by_rk)
        return res

    def save(self, data):
        wechat_id = data['gzh']['wechat_id'].encode("utf-8")
        articles = data['article']
        wechat_name = data['gzh']['wechat_name'].encode("utf-8")
        logger.info("wehchat_id:%s article size:%d", wechat_id, len(articles))
        for article in articles:
            try:
                self._save_one(article, wechat_id, wechat_name)
            except Exception as e:
                logger.warn(e)
                logger.warn(u"save one failed for article:%s", article['title'])

    def get_and_save_article_detail(self, url, article_id, wechat_id, wechat_name, title):
        html = get_html(url)
        if not html:
            return False
        content = format_html(html)
        db.clear_stats()
        db.table("wechat_article_detail").add({
                'article_id': article_id,
                'content_url': url,
                'title': title,
                'wechat_id': wechat_id,
                'wechat_name': wechat_name,
                'html': content
                })
        logger.info("into detail:%s", article_id)
        return True

    def _save_one(self, data, wechat_id, wechat_name):
        db.clear_stats()
        db.where_sql = '''fileid = "%s" and send_id="%s" and wechat_id = "%s" ''' % (data['fileid'], data['send_id'], wechat_id)
        found = db.table(u"wechat_article_profile").find(1)
        if found:
            logger.debug("fileid:%s already in db, ignore", data['fileid'])
            return 

        url = data['content_url'].encode("utf-8")
        title = data['title'].encode("utf-8")
        article_id = gen_article_id(url)

        try:
            succ = self.get_and_save_article_detail(url, article_id, wechat_id, wechat_name, title)
            if not succ:
                logger.warn("article_id:%d get_and_save_article_detail error, url:%s", article_id, url)
                return
        except Exception as e:
            print(e)
            logger.warn("get_and_save_article_detail error:%s", e.message)
            return

        db.clear_stats()
        db.table("wechat_article_profile").add({
                'article_id': article_id,
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
                'wechat_id': wechat_id,
                'wechat_name': wechat_name
                })
        logger.info("into profile:%s", article_id)

        
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
        test = False
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

