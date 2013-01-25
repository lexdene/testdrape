from mako.template import Template
from mako.lookup import TemplateLookup

class View(object):
	def __init__(self,path):
		self.__path = path
		
	def render(self,vardict):
		mylookup = TemplateLookup(
			directories=['app/template'],
			input_encoding='utf-8',
			output_encoding='utf-8',
			encoding_errors='replace'
		)
		#mytemplate = Template(filename='app/template%s.html'%self.__path)
		mytemplate = mylookup.get_template('%s.html'%self.__path)
		return mytemplate.render_unicode(**vardict)
