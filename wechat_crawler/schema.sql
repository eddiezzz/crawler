SET FOREIGN_KEY_CHECKS=0;

create database IF NOT EXISTS techwood_new DEFAULT charset utf8mb4;
use techwood_new;


DROP TABLE IF EXISTS `wechat_mp_crawl`;
CREATE TABLE `wechat_mp_crawl` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `wechat_name` varchar(50) DEFAULT '' COMMENT '要添加的公众号名称',
  `wechat_id` varchar(50) DEFAULT '' COMMENT '公众号的微信号',
  PRIMARY KEY (`_id`),
  UNIQUE KEY (`wechat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `wechat_mp_profile`;
CREATE TABLE `wechat_mp_profile` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'increment id',
  `wechat_name` varchar(30) DEFAULT '' COMMENT 'name',
  `wechat_id` varchar(30) DEFAULT '' COMMENT 'id',
  `headimage` varchar(300) DEFAULT '' COMMENT 'headimage',
  `qrcode` varchar(300) DEFAULT '' COMMENT 'qrcode',
  `introduction` varchar(300) DEFAULT '' COMMENT 'introduction',
  `authentication` varchar(100) DEFAULT '' COMMENT 'authentication',
  `profile_url` varchar(300) DEFAULT '' COMMENT '最近10条群发页链接',
  `post_perm` int(8) DEFAULT 0 COMMENT '最近一月群发数',
  `view_perm` int(8) DEFAULT 0 COMMENT '最近一月阅读量',
  `updatetime` datetime DEFAULT NULL COMMENT 'updatetime',
  PRIMARY KEY (`_id`),
  UNIQUE KEY `wechat_id`(`wechat_id`) 
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `wechat_mp_stat`;

DROP TABLE IF EXISTS `wechat_article_profile`;
CREATE TABLE `wechat_article_profile` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `article_id` varchar(50) NULL COMMENT 'ID',
  `author` varchar(50) DEFAULT '' COMMENT '作者',
  `content_url` varchar(300) DEFAULT '' COMMENT '文章链接',
  `source_url` varchar(500) DEFAULT '' COMMENT '阅读原文链接',
  `copyright_stat` int(1) DEFAULT '0' COMMENT '11表示原创 其它表示非原创',
  `cover_url` varchar(300) DEFAULT '' COMMENT '封面图URL',
  `datetime` datetime DEFAULT NULL COMMENT '文章推送时间',
  `fileid` int(30) DEFAULT '0' COMMENT 'file ID',
  `main` int(11) DEFAULT '0' COMMENT '是否是一次群发的第一次消息 1 or 0',
  `send_id` int(30) DEFAULT '0' COMMENT '群发id，注意不唯一，因为同一次群发多个消息，而群发id一致',
  `title` varchar(300) DEFAULT '' COMMENT '文章标题',
  `type` int(11) DEFAULT '0' COMMENT '消息类型，均是49（在手机端历史消息页有其他类型，网页端最近10条消息页只有49），表示图文', 
  `abstract` varchar(500) DEFAULT '' COMMENT '文章摘要',
  `wechat_id` varchar(50) DEFAULT '0' COMMENT '对应的公众号ID',
  `wechat_name` varchar(30) DEFAULT '' COMMENT 'wechat name',
  PRIMARY KEY (`_id`),
  INDEX `uniq_id`(`send_id`, `fileid`, `wechat_id`),
  INDEX `wechat_id`(`wechat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `wechat_article_stat`;
CREATE TABLE `wechat_article_stat` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `article_id` varchar(50) NULL COMMENT 'ID',
  `updatetime` datetime DEFAULT NULL COMMENT '统计时间',
  `read_count` int(11) DEFAULT '0' COMMENT '新增阅读数',
  `like_count` int(11) DEFAULT '0' COMMENT '新增点攒数',
  `comment_count` int(11) DEFAULT '0' COMMENT '新增评论数',
  PRIMARY KEY (`_id`),
  UNIQUE KEY `article_id`(`article_id`) 
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `user_subs`;
CREATE TABLE `user_subs` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `userid` int(11) NOT NULL COMMENT 'userid',
  `sub_wx` varchar(20) NOT NULL COMMENT '公众号',
  `sub_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '加入订阅时间',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `wechat_article_detail`;
CREATE TABLE `wechat_article_detail` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `title` varchar(300) DEFAULT '' COMMENT '文章标题',
  `article_id` varchar(50) NULL COMMENT 'ID',
  `wechat_name` varchar(30) DEFAULT '' COMMENT 'wechat name',
  `wechat_id` varchar(30) DEFAULT '' COMMENT 'wechat id',
  `content_url` varchar(300) DEFAULT '' COMMENT '文章链接',
  `tag1` varchar(50) DEFAULT '' COMMENT 'machine learning tags',
  `tag1_weight` float(6, 4) DEFAULT '0.0' COMMENT 'machine learning tags',
  `tag2` varchar(50) DEFAULT '' COMMENT 'machine learning tags',
  `tag2_weight` float(6, 4) DEFAULT '0.0' COMMENT 'machine learning tags',
  `tag3` varchar(50) DEFAULT '' COMMENT 'machine learning tags',
  `tag3_weight` float(6, 4) DEFAULT '0.0' COMMENT 'machine learning tags',
  `html` MEDIUMTEXT COMMENT 'html detail',
  PRIMARY KEY (`_id`),
  UNIQUE KEY `article_id`(`article_id`) 
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4;


