import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os, sys, time, operator

from django.core.management import setup_environ
# add the path so Django can apply settings
sys.path.append(os.path.dirname(sys.argv[0]))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.path.pardir)))
# need this for Django models
os.environ['DJANGO_SETTINGS_MODULE'] = 'freshen.settings'

# import the settings.py file
from freshen import settings
setup_environ(settings)

from core.models import Event 
from core.watcher import Processor
from pyinotify import WatchManager, ThreadedNotifier, EventsCodes
from django.db.models import Q

class MainHandler(tornado.web.RequestHandler):
	def initialize(self, blacklist):
		# build the blacklist that will be applied to each query
		qobjs = (~Q(filename__icontains="%s" % (q)) for q in blacklist)
		self.blacklist = reduce(operator.and_, qobjs)
	#
	# get(self) is called when the application receives a GET request
	#
	@tornado.web.asynchronous
	def get(self):
		# JSONP api
		if 'callback' in self.request.arguments:
			# if any files were modified/created/deleted, reload the page
			queue = Event.objects.filter(self.blacklist)
			if len(queue):
				self.write_callback(len(queue))
			else:
				# wait for 20 seconds, if no activity, send response
				def wait_for_events(iteration):
					queue = Event.objects.filter(self.blacklist)
					if iteration >= 40 and not len(queue):
						self.write_callback(0)
					elif len(queue):
						self.write_callback(len(queue))
					else:
						tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 0.5, lambda: wait_for_events(iteration + 1))
				wait_for_events(0)
		else:
			self.write('Invalid request.')
			self.finish()

	#
	# return a response "callback(events)" where events is 0 or non-zero integer
	#
	def write_callback(self, events):
		try:
			self.set_header('Content-Type', 'application/javascript')
			self.set_header('Access-Control-Allow-Origin', '*')
			response = "%s(%s)" % (self.get_argument('callback'), events)
			self.write(response)
			Event.objects.all().delete()
			self.finish()
		except AssertionError:
			pass	

#
# Create the worker to handle all the backend 
#
worker = tornado.web.Application([
	(r'/', MainHandler, dict(blacklist=settings.BLACKLIST)),
])

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Give a path to watch for changes.'
		exit(0)

	Event.objects.all().delete()
	wm = WatchManager()
	notifier = ThreadedNotifier(wm, Processor())
	# add a recursive watch on sys.argv[1]
	wdd = wm.add_watch(sys.argv[1], reduce(operator.or_, [EventsCodes.ALL_FLAGS[mask] for mask in settings.MASK]), rec=True, auto_add=True)

	server = tornado.httpserver.HTTPServer(worker)
	try:
		notifier.start()
		server.listen(9020)
		tornado.ioloop.IOLoop.instance().start()

	except KeyboardInterrupt:
		print '\nSIGTERM received. Shutting down.'
		notifier.stop()
		server.stop()
		tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 2, tornado.ioloop.IOLoop.instance().stop)
		sys.exit()

