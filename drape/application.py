# -*- coding: utf-8 -*-

import os,sys,cgi
import controller
import request
import response
import traceback
import cookie
import session

if sys.getdefaultencoding() != 'utf-8':
	reload(sys)
	sys.setdefaultencoding('utf-8')

class Application(object):
	__singleton = None
	
	@staticmethod
	def singleton():
		return Application.__singleton
		
	@staticmethod
	def setSingleton(singleton):
		Application.__singleton = singleton
		
	def __init__(self):
		self.__request = None
		self.__session = None
		self.__apptype = 'cgi'
		self.__request = request.Request()
		self.__response = response.Response()
		self.env = dict()
		for i in os.environ:
			self.env[i] = os.environ[i]
		self.setSingleton(self)
		
	def start(self):
		self.run()
		
	def run(self):
		try:
			import config
			
			config.update(self.edconfig())
			
			c = config.config
			
			self.__request.run()
			self.__cookie = cookie.Cookie(self)
			
			self.response().addHeader('Content-Type','text/html; charset=utf-8')
			
			path = self.__request.controllerPath()
			
			controllerCls = controller.getControllerClsByPath(path)
			if controllerCls is None:
				controllerCls = NotFound
				
			c = controllerCls(path)
			
			c.run(self.__response)
			
			if not self.__session is None:
				self.__session.save()
				
			self.__cookie.addToHeader(self.__response)
		except Exception as e:
			self.__response.addHeader('Content-Type','text/plain')
			
			body = ''
			body += 'controllerPath:%s\n'%self.__request.controllerPath()
			body += traceback.format_exc()
			body += "environ:\n"
			env = self.env
			for i in env:
				body += "%s => %s\n"%(i,env[i])
			
			self.__response.setBody(body)
			self.__response.setStatus('500 Internal Server Error')
		
	def edconfig(self):
		return dict()
		
	def apptype(self):
		return self.__apptype
		
	def request(self):
		return self.__request
		
	def response(self):
		return self.__response
		
	def cookie(self):
		return self.__cookie
		
	def session(self):
		if self.__session is None:
			self.__session = session.Session(self)
			self.__session.start()
		return self.__session

class WsgiApplication(Application):
	def __init__(self):
		super(WsgiApplication,self).__init__()
		self.__apptype = 'wsgi'
		
	def start(self):
		return
		
	def __call__(self,environ, start_response):
		self.env.update(environ)
		
		self.request().setParams(dict(
			path = self.env['PATH_INFO'],
			root_path = self.env['SCRIPT_NAME'],
			cookie = self.env.get('HTTP_COOKIE'),
			remote_address = self.env['REMOTE_ADDR'],
			field_storage = cgi.FieldStorage(
				fp=self.env['wsgi.input'],
				environ=self.env,
				keep_blank_values=True
			)
		))
		self.run()
		
		write = start_response(
			self.response().status(),
			self.response().headers()
		)
		
		ret = self.response().body().encode('utf-8')
		return ret

class SaeApplication(WsgiApplication):
	def __init__(self):
		super(SaeApplication,self).__init__()
		self.__apptype = 'sae'
		
	def edconfig(self):
		import sae.const
		# sae.const.MYSQL_DB      # 数据库名
		# sae.const.MYSQL_USER    # 用户名
		# sae.const.MYSQL_PASS    # 密码
		# sae.const.MYSQL_HOST    # 主库域名（可读写）
		# sae.const.MYSQL_PORT    # 端口，类型为，请根据框架要求自行转换为int
		# sae.const.MYSQL_HOST_S  # 从库域名（只读）
		config={
			'db' : {
				'dbname' : sae.const.MYSQL_DB ,
				'user' : sae.const.MYSQL_USER ,
				'password' : sae.const.MYSQL_PASS ,
				'host' : sae.const.MYSQL_HOST ,
				'port' : sae.const.MYSQL_PORT,
			},
			'session' : {
				'store_type' : 'memcache',
				'store_args' : {},
			}
		}
		return config
