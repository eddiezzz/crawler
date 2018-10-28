# -*- coding: utf-8 -*-

import wechatsogou

wechat = wechatsogou.WechatSogouAPI(captcha_break_time=3)
#res = wechat.get_gzh_info("tongyipaocha")
res = wechat.get_gzh_article_by_history("tongyipaocha")
print(res)
