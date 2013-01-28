# -*- coding: utf-8 -*-

import frame
import drape
import drape.validate

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

class ajaxRegister(drape.controller.jsonController):
	def process(self):
		aParams = self.params()
		
		# validates
		validates = [
			dict(
				key = 'loginname',
				name = '登录名',
				validates = [
					('notempty',),
					('len',4,20)
				]
			) ,
			dict(
				key = 'password',
				name = '密码',
				validates = [
					('notempty',),
					('len',4,20)
				]
			) ,
			dict(
				key = 'repassword',
				name = '重复密码',
				validates = [
					('notempty',),
					('equal','password','密码')
				]
			) ,
			dict(
				key = 'nickname',
				name = '昵称',
				validates = [
					('notempty',),
					('len',4,20)
				]
			) ,
			dict(
				key = 'nickname',
				name = '昵称',
				validates = [
					('notempty',),
					('len',4,20)
				]
			) ,
			dict(
				key = 'email',
				name = '电子邮箱',
				validates = [
					('notempty',),
					('email',)
				]
			) ,
		]
		
		res = drape.validate.validate_params(aParams,validates)
		if False == res['result']:
			self.setVariable('result','failed')
			self.setVariable('msg',res['msg'])
			return
		
		aLogininfoModel = drape.model.LinkedModel('logininfo')
		res = aLogininfoModel.where(dict(loginname=aParams.get('loginname'))).select()
		if len(res) > 0:
			self.setVariable('result','failed')
			self.setVariable('msg','存在登录名相同的用户，无法注册')
			return
		
		uid = aLogininfoModel.insert(dict(
			loginname = aParams.get('loginname'),
			password = drape.util.md5sum(aParams.get('password'))
		))
		self.setVariable('uid',uid)
		
		aUserinfoModel = drape.model.LinkedModel('userinfo')
		aUserinfoModel.insert(dict(
			uid = uid,
			nickname = aParams.get('nickname'),
			email = aParams.get('email')
		))
		
		self.setVariable('result','success')
