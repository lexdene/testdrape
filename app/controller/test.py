# -*- coding: utf-8 -*-

import os,hashlib
import drape
import frame

class TestFrame(drape.NestingController):
	def __init__(self,path):
		super(TestFrame,self).__init__(path)
		self.setParent('/test/Layout')

class Layout(frame.DefaultFrame):
	def process(self):
		self.initRes()

class Index(TestFrame):
	pass

class Params(TestFrame):
	def process(self):
		aParams = self.params()
		self.setVariable('params',aParams)

class GetFile(TestFrame):
	def process(self):
		key = 'avatar'
		aFiles = self.files()
		
		if key in aFiles:
			myfile = aFiles[key]
			
			sufix = os.path.splitext(myfile.filename)[1][1:]
			
			m = hashlib.sha1()
			m.update(myfile.file.read())
			saveFileName = m.hexdigest()
			
			filepath = '%s.%s'%(saveFileName,sufix)
			
			savepath = self.saveUploadFile(myfile,filepath)
			self.setVariable('savepath',savepath)

class IterFile(TestFrame):
	pass

class Db(TestFrame):
	def process(self):
		aDb = drape.application.Application.singleton().db()
		aParams = self.params()
		res = aDb.query(
			'select * from userinfo where uid>%(uid)s',
			dict(uid=aParams.get('uid',0))
		)
		
		self.setVariable('userlist',res)

class LinkedModel(TestFrame):
	def __init__(self,path):
		super(LinkedModel,self).__init__(path)
		
	def process(self):
		aParams = self.params()
		aModel = drape.LinkedModel('logininfo')
		res = aModel \
			.alias('li') \
			.join('userinfo','ui','ui.uid=li.uid') \
			.select()
		for u in res:
			u['ui.email'] = str(u['ui.email']).replace("@", " at ")
			u['ui.email'] = str(u['ui.email']).replace(".", " dot ")
		self.setVariable('userlist',res)

class IterCookie(TestFrame):
	def process(self):
		aCookie = self.cookie()
		cookies = dict()
		for k,v in aCookie.iteritems():
			cookies[k] = v
		self.setVariable('cookies',cookies)

class GetCookie(TestFrame):
	def process(self):
		aCookie = self.cookie()
		aParams = self.params()
		key = aParams.get('key')
		
		if not key is None:
			cookie = aCookie.get(key)
		else:
			cookie = None
		
		self.setVariable('key',key)
		self.setVariable('cookie',cookie)

class SetCookie(drape.controller.Controller):
	def process(self):
		aParams = self.params()
		key = aParams.get('key')
		value = aParams.get('value')
		expires = aParams.get('expires')
		if not key is None and not value is None:
			aCookie = self.cookie()
			aCookie.add(**self.params())

class IterSession(TestFrame):
	def process(self):
		aSession = self.session()
		sessions = dict()
		for k,v in aSession.iteritems():
			sessions[k] = v
		self.setVariable('sessions',sessions)

class SetSession(TestFrame):
	def process(self):
		aSession = self.session()
		aParams = self.params()
		
		key = aParams.get('key')
		value = aParams.get('value')
		if not key is None and not value is None:
			if len(key) > 20:
				self.setVariable('msg',u'key值长度过长')
			elif len(value) > 20:
				self.setVariable('msg',u'value值长度过长')
			elif key in ('uid',):
				self.setVariable('msg',u'permission denied')
			else:
				self.setVariable('msg','success')
				aSession.set(key,value)
		else:
			self.setVariable('msg','no')
		self.setVariable('key',key)
		self.setVariable('value',value)

class TestSaeConst(TestFrame):
	def process(self):
		import sae.const
		self.setVariable('sae_dir',dir(sae))
		self.setVariable('sae_const_dir',dir(sae.const))
