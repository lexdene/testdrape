# -*- coding: utf-8 -*-

import drape
import frame

class CreateTables(frame.DefaultFrame):
	'''
	Create和Drop不应该放在一起，
	以后应该考虑分开
	'''
	def process(self):
		aDb = drape.application.Application.singleton().db()
		tablePrefix = aDb.tablePrefix()
		tables = {
			'logininfo' :
				'''CREATE TABLE IF NOT EXISTS `%slogininfo` (
					`uid` int NOT NULL AUTO_INCREMENT,
					`loginname` varchar(60) NOT NULL,
					`password` varchar(60) NOT NULL,
					PRIMARY KEY (`uid`),
					UNIQUE KEY `loginname` (`loginname`)
				)ENGINE=MyISAM DEFAULT CHARSET=utf8'''%tablePrefix,
			'userinfo' :
				'''CREATE TABLE IF NOT EXISTS `%suserinfo` (
					`uid` int NOT NULL,
					`nickname` varchar(60) NOT NULL,
					`email` varchar(60) NOT NULL,
					`avatar` varchar(100),
					PRIMARY KEY (`uid`)
				)ENGINE=MyISAM DEFAULT CHARSET=utf8'''%tablePrefix,
			'problem' :
				'''CREATE TABLE IF NOT EXISTS `%sproblem` (
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
				)ENGINE=MyISAM DEFAULT CHARSET=utf8'''%tablePrefix,
			'problem_num' :
				'''CREATE TABLE IF NOT EXISTS `%sproblem_num`(
					`pnum` int NOT NULL AUTO_INCREMENT COMMENT '题号',
					`pid` int NOT NULL COMMENT '题目真实id',
					PRIMARY KEY (`pnum`)
				)AUTO_INCREMENT=1000'''%tablePrefix,
			'permission' :
				'''CREATE TABLE IF NOT EXISTS `%spermission`(
					`id` int NOT NULL AUTO_INCREMENT,
					`uid` int NOT NULL COMMENT '用户id',
					`permission` varchar(20) NOT NULL COMMENT '权限',
					PRIMARY KEY (`id`)
				)'''%tablePrefix,
			'submit' :
				'''CREATE TABLE IF NOT EXISTS `%ssubmit`(
					`id` int NOT NULL AUTO_INCREMENT,
					`pid` int NOT NULL COMMENT '题目id',
					`uid` int NOT NULL COMMENT '用户id',
					`judgeResultId` int NOT NULL COMMENT '结果id，默认为-1',
					`addtime` int NOT NULL COMMENT '添加时间，时间戳',
					`language` varchar(30) NOT NULL COMMENT '语言',
					`code` TEXT NOT NULL,
					PRIMARY KEY (`id`)
				)ENGINE=MyISAM DEFAULT CHARSET=utf8'''%tablePrefix,
			'judge_result' :
				'''CREATE TABLE IF NOT EXISTS `%sjudge_result`(
					`id` int NOT NULL AUTO_INCREMENT,
					`sid` int NOT NULL COMMENT 'submit id',
					`juid` int NOT NULL COMMENT 'judge 用户 id',
					`result` varchar(20) NOT NULL,
					`addtime` int NOT NULL COMMENT '添加时间，时间戳',
					PRIMARY KEY (`id`)
				)ENGINE=MyISAM DEFAULT CHARSET=utf8'''%tablePrefix,
			'user_setting' :
				'''CREATE TABLE IF NOT EXISTS `%suser_setting`(
					`id` int NOT NULL AUTO_INCREMENT,
					`key` varchar(100) NOT NULL,
					`uid` int NOT NULL,
					`value` varchar(100) NOT NULL,
					PRIMARY KEY (`id`),
					INDEX uk ( `key`, `uid` )
				)ENGINE=MyISAM DEFAULT CHARSET=utf8'''%tablePrefix,
			'discuss_topic' :
				'''CREATE TABLE IF NOT EXISTS `%sdiscuss_topic`(
					`id` int NOT NULL AUTO_INCREMENT,
					`pid` int NOT NULL COMMENT '题目id',
					`uid` int NOT NULL COMMENT '用户id',
					`ctime` int NOT NULL COMMENT '创建时间',
					`last_rid` int NOT NULL COMMENT '最后回复reply id',
					`title` varchar(100) NOT NULL COMMENT '标题',
					`text` TEXT NOT NULL COMMENT '正文',
					PRIMARY KEY (`id`)
				)ENGINE=MyISAM DEFAULT CHARSET=utf8'''%tablePrefix,
			'discuss_reply' :
				'''CREATE TABLE IF NOT EXISTS `%sdiscuss_reply`(
					`id` int NOT NULL AUTO_INCREMENT,
					`tid` int NOT NULL COMMENT '主题id',
					`uid` int NOT NULL COMMENT '用户id',
					`reply_to_id` int NOT NULL COMMENT '回复某个回复',
					`ctime` int NOT NULL COMMENT '创建时间',
					`text` TEXT NOT NULL COMMENT '正文',
					PRIMARY KEY (`id`)
				)ENGINE=MyISAM DEFAULT CHARSET=utf8'''%tablePrefix
		}
		
		result = dict()
		section = self.params().get('section')
		for tableName,sql in tables.iteritems():
			if 'drop' == section:
				sql = 'drop table `%s%s`'%(tablePrefix,tableName)
			res = aDb.execute(sql)
			result[tableName] = {
				'sql' : sql,
				'res' : res ,
				'error' : ''
			}
		
		self.setVariable('result',result)
