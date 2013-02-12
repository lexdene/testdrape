# -*- coding: utf-8 -*-

import drape
import frame

class CreateTables(frame.DefaultFrame):
	def process(self):
		tables = {
			'logininfo' :
				'''CREATE TABLE IF NOT EXISTS `logininfo` (
					`uid` int NOT NULL AUTO_INCREMENT,
					`loginname` varchar(60) NOT NULL,
					`password` varchar(60) NOT NULL,
					PRIMARY KEY (`uid`),
					UNIQUE KEY `loginname` (`loginname`)
				)''',
			'userinfo' :
				'''CREATE TABLE IF NOT EXISTS `userinfo` (
					`uid` int NOT NULL,
					`nickname` varchar(60) NOT NULL,
					`email` varchar(60) NOT NULL,
					`avatar` varchar(100),
					PRIMARY KEY (`uid`)
				)ENGINE=MyISAM DEFAULT CHARSET=utf8''',
			'problem' :
				'''CREATE TABLE IF NOT EXISTS `problem` (
					`pid` int NOT NULL AUTO_INCREMENT COMMENT '内部id,题号由时间排序得到',
					`title` varchar(60) NOT NULL COMMENT '题目标题',
					`addtime` int NOT NULL COMMENT '添加时间，时间戳',
					`time_limit` int NOT NULL COMMENT '单位：ms' ,
					`memory_limit` int NOT NULL COMMENT '单位：kb' ,
					`description` TEXT NOT NULL ,
					`input` TEXT NOT NULL,
					`output` TEXT NOT NULL,
					`sample_input` TEXT NOT NULL,
					`sample_output` TEXT NOT NULL,
					`hint` TEXT NOT NULL,
					`source` varchar(100) NOT NULL,
					`authorid` int NOT NULL,
					PRIMARY KEY (`pid`)
				)ENGINE=MyISAM DEFAULT CHARSET=utf8''',
			'problem_num' :
				'''CREATE TABLE IF NOT EXISTS `problem_num`(
					`pnum` int NOT NULL AUTO_INCREMENT COMMENT '题号',
					`pid` int NOT NULL COMMENT '题目真实id',
					PRIMARY KEY (`pnum`)
				)AUTO_INCREMENT=1000''',
			'permission' :
				'''CREATE TABLE IF NOT EXISTS `permission`(
					`id` int NOT NULL AUTO_INCREMENT,
					`uid` int NOT NULL COMMENT '用户id',
					`permission` varchar(20) NOT NULL COMMENT '权限',
					PRIMARY KEY (`id`)
				)''',
			'submit' :
				'''CREATE TABLE IF NOT EXISTS `submit`(
					`id` int NOT NULL AUTO_INCREMENT,
					`pid` int NOT NULL COMMENT '题目id',
					`uid` int NOT NULL COMMENT '用户id',
					`judgeResultId` int NOT NULL COMMENT '结果id，默认为-1',
					`addtime` int NOT NULL COMMENT '添加时间，时间戳',
					`language` varchar(30) NOT NULL COMMENT '语言',
					`code` TEXT NOT NULL,
					PRIMARY KEY (`id`)
				)ENGINE=MyISAM DEFAULT CHARSET=utf8''',
			'judge_result' :
				'''CREATE TABLE IF NOT EXISTS `judge_result`(
					`id` int NOT NULL AUTO_INCREMENT,
					`sid` int NOT NULL COMMENT 'submit id',
					`juid` int NOT NULL COMMENT 'judge 用户 id',
					`result` varchar(20) NOT NULL,
					`addtime` int NOT NULL COMMENT '添加时间，时间戳',
					PRIMARY KEY (`id`)
				)ENGINE=MyISAM DEFAULT CHARSET=utf8''',
			'user_setting' :
				'''CREATE TABLE IF NOT EXISTS `user_setting`(
					`id` int NOT NULL AUTO_INCREMENT,
					`key` varchar(100) NOT NULL,
					`uid` int NOT NULL,
					`value` varchar(100) NOT NULL,
					PRIMARY KEY (`id`),
					INDEX uk ( `key`, `uid` )
				)ENGINE=MyISAM DEFAULT CHARSET=utf8''',
			'discuss_topic' :
				'''CREATE TABLE IF NOT EXISTS `discuss_topic`(
					`id` int NOT NULL AUTO_INCREMENT,
					`pid` int NOT NULL COMMENT '题目id',
					`uid` int NOT NULL COMMENT '用户id',
					`ctime` int NOT NULL COMMENT '创建时间',
					`last_rid` int NOT NULL COMMENT '最后回复reply id',
					`title` varchar(100) NOT NULL COMMENT '标题',
					`text` TEXT NOT NULL COMMENT '正文',
					PRIMARY KEY (`id`)
				)ENGINE=MyISAM DEFAULT CHARSET=utf8''',
			'discuss_reply' :
				'''CREATE TABLE IF NOT EXISTS `discuss_reply`(
					`id` int NOT NULL AUTO_INCREMENT,
					`tid` int NOT NULL COMMENT '主题id',
					`uid` int NOT NULL COMMENT '用户id',
					`reply_to_id` int NOT NULL COMMENT '回复某个回复',
					`ctime` int NOT NULL COMMENT '创建时间',
					`text` TEXT NOT NULL COMMENT '正文',
					PRIMARY KEY (`id`)
				)ENGINE=MyISAM DEFAULT CHARSET=utf8'''
		}
		result = dict()
		aDb = drape.application.Application.singleton().db()
		for tableName,sql in tables.iteritems():
			res = aDb.execute(sql)
			result[tableName] = {
				'res' : res ,
				'error' : ''
			}
		
		self.setVariable('sql',tables)
		self.setVariable('result',result)
