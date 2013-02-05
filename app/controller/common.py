# -*- coding: utf-8 -*-

import os,hashlib
import drape
import frame

class UploadImage(frame.EmptyFrame):
	def process(self):
		self.initRes()

class UploadImageResult(frame.EmptyFrame):
	def process(self):
		self.initRes()
		
		key = 'file'
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
			self.setVariable('result','success')
