import drape
import math

class Pager(drape.NestingController):
	def __init__(self,total_count,current_page,item_per_page=10,pager_width=5):
		super(Pager,self).__init__('/widget/Pager')
		self.__total_count = total_count
		self.__current_page = current_page
		self.__item_per_page = item_per_page
		self.__pager_width = pager_width
	
	def limit(self):
		return dict(
			length = self.__item_per_page,
			offset = self.__current_page*self.__item_per_page
		)
	
	def process(self):
		self.setVariable('page_count',int(math.ceil(self.__total_count*1.0/self.__item_per_page)))
		self.setVariable('current_page',self.__current_page)
		self.setVariable('total_count',self.__total_count)
