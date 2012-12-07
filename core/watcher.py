from pyinotify import ProcessEvent
from core.models import Event
import os

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
