import util

config={
	'db' : {
		'driver' : 'mysql' ,
		'dbname' : '' ,
		'user' : '' ,
		'password' : '' ,
		'host' : '' ,
		'port' : '' ,
		'charset' : 'utf8' ,
	},
	'session' : {
		'store_type' : 'file',
		'store_args' : {
			'directory' : 'data/session',
		},
		'cookie_name': 'drape_session_id',
		'cookie_domain': None,
		'timeout': 86400, #24 * 60 * 60, # 24 hours in seconds
		'ignore_expiry': True,
		'ignore_change_ip': True,
		'secret_key': 'fLjUfxqXtfNoIldA0A0J',
		'expired_message': 'Session expired',
	},
	'view' : {
		'template_type' : 'jinja2',
	}
}

def update(newconfig):
	global config
	util.deepmerge(config,newconfig)

try:
	import app.config.config as appconfig
	update(appconfig.config)
except ImportError:
	pass
