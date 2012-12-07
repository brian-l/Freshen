import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os, sys, math, json, time

from django.core.management import setup_environ
# add the path so Django can apply settings
sys.path.append(os.path.dirname(sys.argv[0]))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.path.pardir)))
# need this for Django models
os.environ['DJANGO_SETTINGS_MODULE'] = 'freshen.settings'

#import the settings.py file
from freshen import settings
setup_environ(settings)

from core.models import Event 

class MainHandler(tornado.web.RequestHandler):
	#
	# get(self) is called when the application receives a GET request
	#
	@tornado.web.asynchronous
	def get(self):
		if 'callback' in self.request.arguments:
			queue = Event.objects.all()
			if len(queue):
				self.set_header('Content-Type', 'application/javascript')
				self.set_header('Access-Control-Allow-Origin', '*')
				self.write("%s(%s)" % (self.get_argument('callback'), '0'))
				self.finish()
			else:
				tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 0.5, self.get)
		else:
			self.write('[]')
			self.finish()
#
# Create the worker to handle all the backend 
#
worker = tornado.web.Application([
	(r'/', MainHandler),
])

if __name__ == '__main__':
	# create server and start it on port 8000
	server = tornado.httpserver.HTTPServer(worker)
	try:
		server.listen(9020)
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt:
		print '\nSIGTERM received. Shutting down.'
		server.stop()
		tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 2, tornado.ioloop.IOLoop.instance().stop)
		sys.exit()

