# -*- coding: utf-8 -*-

import frame
import drape

class Login(frame.DefaultFrame):
	def process(self):
		self.initRes()
		self.setTitle(u'登录')
		
		aParams = self.params()
		
		redirect = aParams.get('redirect','/')
		self.setVariable('redirect',redirect)

class ajaxLogin(drape.controller.jsonController):
	def process(self):
		aLoginModel = drape.LinkedModel('logininfo')
		
		res = aLoginModel \
			.where(dict(
				loginname=self.param('loginname')
			)) \
			.select()
		
		if len(res) > 0 and \
			res[0]['password'] == drape.util.md5sum(self.param('password','')):
			self.setVariable('result','success')
		else:
			self.setVariable('result','failed')
			self.setVariable('msg',u'登录名或密码错误')

class Register(frame.DefaultFrame):
	def process(self):
		self.initRes()
		self.setTitle(u'注册')
