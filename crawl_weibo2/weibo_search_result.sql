CREATE TABLE `weibo_search_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_name` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `post_user` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `post_month` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `repost_cnt` int(11) DEFAULT NULL COMMENT 'ת������',
  `thumbs_up_cnt` int(11) DEFAULT NULL COMMENT '��������',
  `reply_cnt` int(11) DEFAULT NULL COMMENT '�ظ�����',
  `t_when` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `content` varchar(4000) character set utf8mb4 collate utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_post` (`post_user`,`post_month`,`t_when`,`game_name`) USING BTREE COMMENT 'ÿ��ÿ����ͬһ��ʱ���ֻ�ܷ�һ������'
) ENGINE=InnoDB AUTO_INCREMENT=36803 DEFAULT CHARSET=utf8 COMMENT='΢���������'
