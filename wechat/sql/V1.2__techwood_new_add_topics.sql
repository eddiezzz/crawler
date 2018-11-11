CREATE TABLE `wechat_mp_crawl` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `wechat_name` varchar(50) DEFAULT '' COMMENT '要添加的公众号名称',
  `wechat_id` varchar(50) DEFAULT '' COMMENT '公众号的微信号',
  PRIMARY KEY (`_id`),
  UNIQUE KEY (`wechat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
