import view
import application
import json

def getControllerClsByPath(path):
	x = path.split('/')
	mod = x[1]
	cls = x[2]
	mod = 'app.controller.%s'%mod
	mod = __import__(mod, globals(), locals(), [""])
	cls = getattr(mod, cls)
	
	return cls

def getControllerByPath(path):
	cls = getControllerClsByPath(path)
	return cls(path)

class Controller(object):
	__globalVars = dict(aaa='bbb')
	def __init__(self,path):
		self.__path = path
		self.__vars = dict()
		
	def run(self,aResponce):
		self.process()
		aResponce.setBody(self.render())
		
	def process(self):
		pass
		
	def render(self):
		return ''
		
	def setVariable(self,name,value):
		self.__vars[name] = value
		
	def variable(self,name):
		return self.__vars[name]
		
	def getVardict(self):
		return self.__vars
		
	@classmethod
	def globalVars(cls):
		return cls.__globalVars
		
	def path(self):
		return self.__path
		
	def params(self):
		aRequest = application.Application.singleton().request()
		return aRequest.params()
		
	def cookie(self):
		return application.Application.singleton().cookie()
		
	def session(self):
		return application.Application.singleton().session()

class ViewController(Controller):
	def __init__(self,path,templatePath=None):
		super(ViewController,self).__init__(path)
		if templatePath is None:
			templatePath = path
		self.__templatePath = templatePath
		
		aRequest = application.Application.singleton().request()
		self.setVariable('ROOT',aRequest.rootPath())
		
		self.setVariable('ctrl',self)
	
	def setTemplatePath(self,templatePath):
		self.__templatePath = templatePath
		
	def render(self):
		aView = view.View(self.__templatePath)
		r = aView.render(self.getVardict())
		return r
		
	def setTitle(self,t):
		g = self.globalVars()
		g['title'] = t
		
class NestingController(ViewController):
	def __init__(self,path):
		super(NestingController,self).__init__(path)
		self.__children = dict()
		self.__parent = None
		
		# cache
		self.__cacheRoot = None
		
	def setNestData(self,nestdata):
		self.__nestdata = nestdata
		
	def nestData(self):
		return self.__nestdata
		
	def buildNest(self):
		def build(nest):
			if isinstance(nest,NestingController):
				return nest
			path = nest['_path']
			aCtrl = getControllerByPath(path)
			
			keywords = ('_path','_name')
			for key,childnest in nest.iteritems():
				if key not in keywords:
					aChildCtrl = build(childnest)
					aCtrl.addChild(key,aChildCtrl)
			
			return aCtrl
			
		return build(self.nestData())
		
	def addChild(self,name,aChildCtrl):
		self.__children[name] = aChildCtrl
		aChildCtrl.setParent(self)
		
	def setParent(self,parent):
		self.__parent = parent
		
	def getRootController(self):
		if self.__parent is None:
			return self
		if self.__cacheRoot is None:
			self.__cacheRoot = self.__parent.getRootController()
			
		return self.__cacheRoot
		
	def children(self):
		return self.__children.iteritems()
		
	def run(self,aResponce):
		self.buildNest()
		
		root = self.getRootController()
		aResponce.setBody(root.nestRun())
		
	def nestRun(self):
		self.beforeChildProcess()
		
		childResult = dict()
		for name,aCtrl in self.children():
			self.setVariable(name,aCtrl.nestRun())
		
		self.process()
		return self.render()
		
	def beforeChildProcess(self):
		pass
		
	def initRes(self):
		g = self.globalVars()
		if 'res' not in g:
			g['res'] = list()
		
		myres = list()
		g['res'].append(myres)
		self.setVariable('res',myres)
		
	def addResByPath(self,type='both'):
		# remove prefix /
		path = self.path()
		
		res = self.variable('res')
		
		if type in ['both','css']:
			res.append(('css%s'%path,'css'))
		if type in ['both','js']:
			res.append(('js%s'%path,'js'))

class jsonController(Controller):
	def render(self):
		return json.dumps(self.getVardict())
