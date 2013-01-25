import cgi

class Request(object):
	def __init__(self):
		self.__controllerPath = None
		# self.path = '/'
		# self.script_name = '/'
		# self.cookie = None
		# self.remote_address = '127.0.0.1'
		
	def setParams(self,params):
		self.__path = params.get('path')
		self.__root_path = params.get('root_path')
		self.__cookie = params.get('cookie')
		self.__remote_address = params.get('remote_address')
		
	def run(self):
		# controller path
		#if os.environ.has_key('PATH_INFO'):
		#	path = os.environ['PATH_INFO']
		#else:
		#	path = '/'
		
		x = self.__path.split('/')
		if len(x) > 1 and x[1] != '':
			mod = x[1]
		else:
			mod = 'index'
		
		if len(x) > 2 and x[2] != '':
			cls = x[2]
		else:
			cls = 'Index'
		
		self.__controllerPath = '/%s/%s'%(mod,cls)
		
		# root path
		# x = self.__script_name.split('/')
		
		# self.__root_path = '/'.join(x[0:-1])
		
		# params
		self.__paramDict = dict()
		
		# path params
		
		# field storage
		# form = cgi.FieldStorage()
		# for i in form:
		#	self.__paramDict[form[i].name] = form[i].value
		
		# cookie
		
		
		# remote address
		# self.__remote_address = os.environ['REMOTE_ADDR']
		
	def controllerPath(self):
		return self.__controllerPath
		
	def rootPath(self):
		return self.__root_path
		
	def remote_address(self):
		return self.__remote_address
		
	def params(self):
		return self.__paramDict
		
	def cookie(self):
		return self.__cookie
