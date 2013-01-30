# -*- coding: utf-8 -*-

import drape
import app

class DefaultFrame(drape.NestingController):
	def __init__(self,path):
		super(DefaultFrame,self).__init__(path)
		
		self.setParent('/frame/Layout')
		
	def notLogin(self):
		self.icRedirect('/frame/NotLogin')

class HtmlBody(drape.NestingController):
	def beforeChildProcess(self):
		g = self.globalVars()
		g.clear()
		g['res'] = list()
		
	def process(self):
		# res
		g = self.globalVars()
		self.setVariable('reslist',reversed( g['res'] ))
		
		# title
		sitename = u'JDMD Online Judge'
		subtitle = u'无标题'
		if 'title' in g:
			subtitle = g['title']
		title = '%s - %s'%(subtitle,sitename)
		self.setVariable('title',title)
		
		# version
		self.setVariable('version',app.version)
		self.setVariable('drape_version',drape.version)
		
		# user id
		self.setVariable('my_userid',-1)

class Layout(drape.NestingController):
	def __init__(self,path):
		super(Layout,self).__init__(path)
		self.setParent('/frame/HtmlBody')
		
	def process(self):
		self.initRes()
		
		aSession = self.session()
		uid = aSession.get('uid',-1)
		self.setVariable('uid',uid)
		
		if uid > 0:
			aUserinfoModel = drape.LinkedModel('userinfo')
			userinfo = aUserinfoModel.where(dict(uid=uid)).find()
			self.setVariable('userinfo',userinfo)

class NotLogin(DefaultFrame):
	def process(self):
		self.initRes()
		urlPath = self.request().urlPath()
		self.setVariable('urlPath',urlPath)
		self.setVariable('urlquote',drape.util.urlquote(urlPath))
