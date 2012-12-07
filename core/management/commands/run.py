from django.core.management.base import AppCommand
from pyinotify import WatchManager, Notifier, EventsCodes, ProcessEvent
from core.watcher import Processor, remote_worker
from core.models import Event
from core.sftp import SFTPConnection 
from optparse import make_option
import threading, os, sys

class Command(AppCommand):
	option_list = AppCommand.option_list + (
			make_option('--path', '-p', dest='path', help="Give a path to watch.",),
			)

	def handle(self, *args, **options):
		if not options['path']:
			print "Provide a correct path to the --path argument."
			sys.exit(1)
		if not os.path.isdir(options['path']):
			print "Provide a correct path to the --path argument."
			sys.exit(1)

		wm = WatchManager()
		mask = EventsCodes.ALL_FLAGS['IN_CREATE'] | EventsCodes.ALL_FLAGS['IN_MODIFY'] | EventsCodes.ALL_FLAGS['IN_DELETE']
		# start the pyinotify thread
		notifier = Notifier(wm, Processor())

		try:
			wdd = wm.add_watch(options['path'], mask, rec=True, auto_add=True)
			while True:
				notifier.process_events()
				if notifier.check_events():
					notifier.read_events()
		except KeyboardInterrupt:
			print "Stopping notifier."
			notifier.stop()
			# to stop the remote thread, set an event mask to -1
			e = Event(filename="/dev/null", type=-1)
			e.save()
			Event.objects.all().delete()
