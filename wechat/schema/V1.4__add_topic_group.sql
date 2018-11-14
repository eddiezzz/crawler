use techwood_new;

CREATE TABLE `group_profile` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'increment id',
  `name` varchar(100) NOT NULL COMMENT 'name',
  `avartar` varchar(100) DEFAULT '' COMMENT 'avartar',
  `intro` TEXT COMMENT 'introduction',
  `type` tinyint DEFAULT 0 COMMENT 'type: operate:0, ugc:1',
  `updatetime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'updatetime',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `group_sites_relation` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'increment id',
  `group_id` int(11) NOT NULL COMMENT 'group id',
  `site_id` int(11) NOT NULL COMMENT 'id',
  `updatetime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'updatetime',
  PRIMARY KEY (`_id`),
  UNIQUE KEY `uniqid`(`group_id`, `site_id`) 
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `group_request` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'increment id',
  `user_id` varchar(30) NOT NULL COMMENT 'user request',
  `group_id` int(11) NOT NULL COMMENT 'group id',
  `group_name` varchar(100) DEFAULT '' COMMENT 'new group name',
  `intro` varchar(300) DEFAULT '' COMMENT 'introduction',
  `updatetime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'updatetime',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `group_stat` (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'increment id',
  `weight` int(8) DEFAULT 0 COMMENT '圈子重要权重: 0~10000 by operate, 10000+ by autoset',
  `post` int(8) DEFAULT 0 COMMENT '总阅读量',
  `view` int(8) DEFAULT 0 COMMENT '最近一月阅读量',
  `like` int(8) DEFAULT 0 COMMENT '最近一月阅读量',
  `month_post` int(8) DEFAULT 0 COMMENT '总阅读量',
  `month_view` int(8) DEFAULT 0 COMMENT '最近一月阅读量',
  `month_like` int(8) DEFAULT 0 COMMENT '最近一月阅读量',
  `updatetime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'updatetime',
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;

