# -*- coding: utf-8 -*-

import time

import frame
import drape
import drape.validate
import markdown

class List(frame.DefaultFrame):
	def process(self):
		self.initRes()
		self.setTitle(u'讨论区')
		
		aParams = self.params()
		pnum = drape.util.toInt(aParams.get('pnum',-1))
		where = dict()
		if pnum > 0:
			where['pn.pnum'] = pnum
		
		aTopicModel = drape.LinkedModel('discuss_topic')
		aTopicList = aTopicModel \
			.alias('dt') \
			.join('problem_num','pn','dt.pid = pn.pid') \
			.join('userinfo','topic_ui','dt.uid = topic_ui.uid') \
			.join('discuss_reply','last_dr','last_dr.tid = dt.id AND last_dr.id = dt.last_rid') \
			.join('userinfo','last_dr_ui','last_dr.uid = last_dr_ui.uid') \
			.join('discuss_reply','count_dr','count_dr.tid = dt.id') \
			.where(where) \
			.group('dt.id') \
			.field('COUNT(count_dr.id)') \
			.reflectField(['dt','pn','topic_ui','last_dr','last_dr_ui']) \
			.order('CASE WHEN last_dr.id is NULL THEN dt.ctime ELSE last_dr.ctime END DESC') \
			.select()
		
		for aTopic in aTopicList:
			aTopic['ctime_str'] = drape.util.timeStamp2Short(aTopic['ctime'])
			aTopic['last_dr.ctime_str'] = drape.util.timeStamp2Short(aTopic['last_dr.ctime'])
		
		self.setVariable('pnum',pnum)
		self.setVariable('iter',aTopicList)

class PostTopic(frame.DefaultFrame):
	def process(self):
		self.initRes()
		self.setTitle(u'发表新主题')
		
		aSession = self.session()
		uid = aSession.get('uid',-1)
		if uid < 0:
			self.notLogin()
		
		aParams = self.params()
		pnum = drape.util.toInt(aParams.get('pnum',-1))
		self.setVariable('pnum',pnum)

class ajaxPostTopic(drape.controller.jsonController):
	def process(self):
		aSession = self.session()
		uid = aSession.get('uid',-1)
		if uid < 0:
			self.setVariable('result','failed')
			self.setVariable('msg','请先登录')
			return
		
		aParams = self.params()
		# validates
		validates = [
			dict(
				key = 'pnum',
				name = '题号',
				validates = [
					('int',),
				]
			) ,
			dict(
				key = 'title',
				name = '标题',
				validates = [
					('notempty',),
					('len',4,50)
				]
			) ,
			dict(
				key = 'text',
				name = '内容',
				validates = [
					('notempty',),
					('len',4,500)
				]
			) ,
		]
		res = drape.validate.validate_params(aParams,validates)
		if False == res['result']:
			self.setVariable('result','failed')
			self.setVariable('msg',res['msg'])
			return
		
		pnum = drape.util.toInt(aParams.get('pnum',-1))
		if pnum > 0 :
			aPnumModel = drape.LinkedModel('problem_num')
			problem = aPnumModel.where(dict(pnum=pnum)).find()
			
			if problem is None:
				self.setVariable('result','failed')
				self.setVariable('msg',u'pnum错误:没有此题')
				return
			else:
				pid = problem['pid']
		else:
			pid = -1
		
		aDiscussModel = drape.LinkedModel('discuss_topic')
		aDiscussModel.insert(dict(
			pid = pid,
			uid = uid,
			ctime = int( time.time() ),
			last_rid = -1,
			title = aParams.get('title',''),
			text = aParams.get('text','')
		))
		
		self.setVariable('result','success')
		self.setVariable('msg',u'发表成功')

class Topic(frame.DefaultFrame):
	def process(self):
		self.initRes()
		
		aParams = self.params()
		tid = drape.util.toInt(aParams.get('id',-1))
		if tid < 0:
			self.Error(u'参数无效:缺少id参数或id参数不是整数')
			return
		
		aDiscussModel = drape.LinkedModel('discuss_topic')
		aTopicInfo = aDiscussModel \
			.alias('dt') \
			.join('userinfo','ui','dt.uid = ui.uid') \
			.join('problem_num','pn','dt.pid = pn.pid') \
			.where({'dt.id':tid}) \
			.find()
		
		if aTopicInfo is None:
			self.Error(u'参数无效:没有与id对应的主题')
			return
		
		aTopicInfo['ctime_str'] = drape.util.timeStamp2Str(aTopicInfo['ctime'])
		aTopicInfo['text'] = markdown.markdown( aTopicInfo['text'] )
		self.setVariable('topicInfo',aTopicInfo)
		self.setTitle(aTopicInfo['title'])
		
		aReplyModel = drape.LinkedModel('discuss_reply')
		aReplyIter = aReplyModel \
			.alias('dr') \
			.join('userinfo','ui','dr.uid = ui.uid') \
			.where({'dr.tid':tid}) \
			.select()
		for c,reply in enumerate(aReplyIter):
			reply['floor'] = c+2
			reply['ctime_str'] = drape.util.timeStamp2Str(reply['ctime'])
			reply['text'] = markdown.markdown( reply['text'] )
		
		self.setVariable('aReplyIter',aReplyIter)

class ajaxPostReply(drape.controller.jsonController):
	def process(self):
		aSession = self.session()
		uid = aSession.get('uid',-1)
		if uid < 0:
			self.setVariable('result','failed')
			self.setVariable('msg','请先登录')
			return
		
		aParams = self.params()
		# validates
		validates = [
			dict(
				key = 'tid',
				name = '主题id',
				validates = [
					('int',),
				]
			) ,
			dict(
				key = 'reply_to_id',
				name = '回复id',
				validates = [
					('int',),
				]
			) ,
			dict(
				key = 'text',
				name = '内容',
				validates = [
					('notempty',),
					('len',4,500)
				]
			) ,
		]
		res = drape.validate.validate_params(aParams,validates)
		if False == res['result']:
			self.setVariable('result','failed')
			self.setVariable('msg',res['msg'])
			return
		
		tid = drape.util.toInt( aParams.get('tid',-1) )
		aReplyModel = drape.LinkedModel('discuss_reply')
		reply_id = aReplyModel.insert(dict(
			tid = tid,
			uid = uid,
			reply_to_id = aParams.get('reply_to_id',-1),
			ctime = int( time.time() ),
			text = aParams.get('text',-1),
		))
		
		aTopicModel = drape.LinkedModel('discuss_topic')
		aTopicModel.where(dict(
			id=tid
		)).update(dict(
			last_rid = reply_id
		))
		
		self.setVariable('result','success')
		self.setVariable('msg',u'回复成功')
