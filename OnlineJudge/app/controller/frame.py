# -*- coding: utf-8 -*-

import drape
import app

class DefaultFrame(drape.NestingController):
	def __init__(self,path):
		super(DefaultFrame,self).__init__(path)
		
		self.setNestData({
			'_path':'/frame/HtmlBody',
			'body':{
				'_path':'/frame/Layout',
				'body':self
			}
		})

class HtmlBody(drape.NestingController):
	def beforeChildProcess(self):
		g = self.globalVars()
		if 'res' not in g:
			g['res'] = list()
		
	def process(self):
		# res
		g = self.globalVars()
		self.setVariable('reslist',g['res'])
		
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
	def process(self):
		self.initRes()
