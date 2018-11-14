use techwood_new;

CREATE TABLE `topics` (
  `_id` int NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `name` varchar(50) NOT NULL COMMENT 'topic name',
  `icon` varchar(200) DEFAULT '' COMMENT 'topic icon url',
  `intro` TEXT COMMENT 'topic introduction',
  `weight` int DEFAULT 0 COMMENT 'topic sort weight',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `topics_cluster` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `topic_id` int NOT NULL COMMENT 'topic id in topics._id',
  `site_id` int(11) NOT NULL COMMENT 'site id, wechat_mp_profile._id',
  `site_type` int NOT NULL DEFAULT 0 COMMENT 'site type:0 wechat_mp, 1:rss',
  `weight` int DEFAULT 0 COMMENT 'sort weight',
  `updatetime` datetime DEFAULT NULL COMMENT 'updatetime',
  PRIMARY KEY (`_id`),
  KEY `topic_id`(`topic_id`) 
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `rss_site_profile` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID, site_id',
  `name` varchar(30) NOT NULL COMMENT 'name',
  `headimage` varchar(300) DEFAULT '' COMMENT 'headimage',
  `introduction` varchar(300) DEFAULT '' COMMENT 'introduction',
  `post_perm` int DEFAULT 0 COMMENT '最近一月群发数',
  `view_perm` int DEFAULT 0 COMMENT '最近一月阅读量',
  `plat` varchar(50) DEFAULT '' COMMENT 'bytedance, csdn, someblog...',
  `plat_url` varchar(300) DEFAULT '' COMMENT 'bytedance, csdn, someblog...',
  `updatetime` datetime DEFAULT NULL COMMENT 'updatetime',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4;


ALTER TABLE wechat_mp_profile change post_perm post_perm int DEFAULT 0 COMMENT '最近一月群发数';
ALTER TABLE wechat_mp_profile change view_perm view_perm int DEFAULT 0 COMMENT '最近一月阅读量';

