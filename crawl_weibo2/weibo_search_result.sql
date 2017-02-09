CREATE TABLE `weibo_search_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_name` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `post_user` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `post_month` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `repost_cnt` int(11) DEFAULT NULL COMMENT '转发数量',
  `thumbs_up_cnt` int(11) DEFAULT NULL COMMENT '点赞数量',
  `reply_cnt` int(11) DEFAULT NULL COMMENT '回复数量',
  `t_when` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `content` varchar(4000) character set utf8mb4 collate utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_post` (`post_user`,`post_month`,`t_when`,`game_name`) USING BTREE COMMENT '每人每个月同一个时间点只能发一条数据'
) ENGINE=InnoDB AUTO_INCREMENT=36803 DEFAULT CHARSET=utf8 COMMENT='微博搜索结果'
