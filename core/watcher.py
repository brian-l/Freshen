from pyinotify import WatchManager, Notifier, EventsCodes, ProcessEvent
from core.models import Event
from django.db.models.aggregates import Max
import os, threading, time, sys

import logging
#logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

# the function to call for the thread that will send data up to the main server.
def remote_worker(sftp):
	if threading.currentThread().getName() != "Remote":
		logging.debug("Thread already running")
		sys.exit(1)
	else:
		while True:
			events = dict()
			for e in Event.objects.all():
				if e.type == -1:
					sys.exit(1)
				key = e.get_key()
				if not events.get(key):
					events[key] = [e.filename]
				elif not e.filename in events[key]:
					events[key].append(e.filename)
			for ev in events:
				sftp.handle_event(ev, events[ev])
			Event.objects.all().delete()
			time.sleep(5)


# when adding a new method to the Processor class, simply add this decorator
# and an Event object will be created
class create(object):
	def __init__(self, func):
		self.func = func
	def __call__(self, *args):
		event = args[0]
		ev = Event(filename=os.path.join(event.path, event.name), type=event.mask)
		ev.save()

class Processor(ProcessEvent):
	@create
	def process_IN_CREATE(self, event):
		pass
	@create
	def process_IN_MODIFY(self, event):
		pass
	@create
	def process_IN_DELETE(self, event):
		pass
	@create
	def process_IN_DELETE_SELF(self, event):
		pass
	@create
	def process_IN_ISDIR(self, event):
		pass
