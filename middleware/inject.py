import settings
from lxml import html, etree

class ScriptInject():
	def process_response(self, request, response):
		# is this a development environment?
		if hasattr(settings, 'DEVELOPMENT'):
			if settings.DEVELOPMENT == True:
				# is the response valid?
				if response.has_header('Content-type'):
					# don't try to inject a script into non-HTML
					if 'html' in response.get('Content-type'):
						tree = html.fromstring(response.content)
						head = tree.find('head')
						# if this is false the content is malformed, skip it
						if head:
							print head
							# create the freshen script element
							freshen_script = etree.SubElement(head, 'script', type='text/javascript', charset='utf-8', src='%sfreshen.js' % (settings.STATIC_URL))

							response.content = html.tostring(tree, pretty_print=True)

		return response
