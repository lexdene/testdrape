import urllib
import hashlib

def urlquote(s):
	return urllib.quote(s)
	
def deepmerge(target,source):
	for k in target :
		if k in source:
			if isinstance( target[k] ,dict ):
				deepmerge(target[k],source[k])
			else:
				target[k] = source[k]

def md5sum(s):
	m = hashlib.md5()
	m.update(s)
	return m.hexdigest()
