from django.db import models
from pyinotify import EventsCodes

class Event(models.Model):
	# absolute file name
	filename = models.CharField(default='', max_length=512)
	# integer as defined by inotify. ie: IN_CREATE = 256, IN_MODIFY = 2, IN_DELETE = 512
	# see pyinotify.EventsCodes.ALL_FLAGS for more 
	type = models.IntegerField(default=0)
	# timestamp of when the event occured
	timestamp = models.TimeField(auto_now_add=True)

	def get_key(self):
		type = [k for k, v in EventsCodes.ALL_FLAGS.iteritems() if v & self.type][0]
		print type
		return type

	def __str__(self):
		return "%s %s %s" % (self.filename, self.get_key(), self.timestamp)
