# -*- coding: utf-8 -*-

# system import
import os,sys,cgi,traceback

# drape import
import controller,db,config
import request
import response
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
		self.__apptype = 'cgi'
		self.setSingleton(self)
		self.systemInit()
		
	def systemInit(self):
		'''
		系统级初始化，
		这函数理论上讲应该仅在开机/启动服务器的时候执行一次，以后就不再执行了。
		'''
		config.update(self.edconfig())
		
	def requestInit(self):
		'''
		请求级初始化，
		这函数在每次请求的时候都会执行一次
		'''
		self.__request = request.Request()
		self.__response = response.Response()
		self.__session = None
		self.__cookie = cookie.Cookie(self)
		self.__db = None
		
		g = controller.Controller.globalVars()
		g.clear()
		
	def start(self):
		self.run()
		
	def run(self,environ,params):
		try:
			self.requestInit()
			
			self.__request.run(params,environ)
			
			if self.__request.requestUri() == self.__request.rootPath():
				self.__response.setStatus('301 Moved Permanently')
				self.response().addHeader('Location',self.__request.rootPath() + '/' )
				return
			self.__cookie.run()
			
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
			env = environ
			for i in env:
				body += "%s => %s\n"%(i,env[i])
			
			print body
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
		
	def db(self):
		if self.__db is None:
			self.__db = db.Db()
		return self.__db
		
	def saveUploadFile(self,fileobj,filepath):
		pass

class WsgiApplication(Application):
	def __init__(self):
		super(WsgiApplication,self).__init__()
		self.__apptype = 'wsgi'
		
	def start(self):
		return
		
	def __call__(self,environ, start_response):
		params = dict(
			path = environ['PATH_INFO'],
			root_path = environ['SCRIPT_NAME'],
			cookie = environ.get('HTTP_COOKIE'),
			remote_address = environ['REMOTE_ADDR'],
			field_storage = cgi.FieldStorage(
				fp=environ['wsgi.input'],
				environ=environ,
				keep_blank_values=True
			)
		)
		self.run(environ,params)
		
		ret = self.response().body()
		if isinstance(ret, unicode):
			ret = ret.encode('utf-8')
			self.response().addHeader('Content-Length',str(len(ret)))
		elif isinstance(ret, str):
			ret = ret
			self.response().addHeader('Content-Length',str(len(ret)))
		else:
			ret = str(ret)
		
		write = start_response(
			self.response().status(),
			self.response().headers()
		)
		
		return [ret]
		
	def saveUploadFile(self,fileobj,filepath):
		dirpath = 'static/userupload'
		
		if not os.path.isdir(dirpath):
			os.makedirs(dirpath)
		
		filepath = os.path.join(dirpath,filepath)
		fout = open( filepath ,'w')
		fileobj.file.seek(0)
		fout.write( fileobj.file.read() )
		fout.close()
		return '/'+filepath

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
				'store_args' : None,
			}
		}
		return config
		
	def saveUploadFile(self,fileobj,filepath):
		import sae.storage
		# 初始化一个Storage客户端。
		s = sae.storage.Client()
		# LIST所有的domain
		# s.list_domain()
		# PUT object至某个domain下面，put操作返回object的public url。
		fileobj.file.seek(0)
		ob = sae.storage.Object(fileobj.file.read())
		domain_name = config.config['sae_storage']['domain_name']
		return s.put(domain_name, filepath, ob)
