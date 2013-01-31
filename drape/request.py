class Request(object):
	def __init__(self):
		self.__controllerPath = None
		
	def run(self,params,env):
		# url path
		self.__urlPath = params.get('path')
		qs = env.get('QUERY_STRING')
		if not qs is None and len(qs) > 0 :
			self.__urlPath += '?'+qs
		
		# controller path
		x = params.get('path').split('/')
		if len(x) > 1 and x[1] != '':
			mod = x[1]
		else:
			mod = 'index'
		
		if len(x) > 2 and x[2] != '':
			cls = x[2]
		else:
			cls = 'Index'
		
		self.__controllerPath = '/%s/%s'%(mod,cls)
		
		# params
		self.__paramDict = dict()
		
		# path params
		i = 3
		while i+1 < len(x):
			key = x[i]
			value = x[i+1]
			self.__paramDict[ key ] = value
			i = i+2
		
		# field storage
		form = params.get('field_storage')
		for i in form:
			self.__paramDict[form[i].name] = form[i].value
		
		self.__root_path = params.get('root_path')
		self.__cookie = params.get('cookie')
		self.__remote_address = params.get('remote_address')
		
	def urlPath(self):
		return self.__urlPath
		
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
