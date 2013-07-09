import settings
from lxml import html, etree

class ScriptInject():
    def process_response(self, request, response):
        # is this a development environment?
        try:
            if settings.DEVELOPMENT == True and 'html' in response['Content-type']:
                tree = html.fromstring(response.content)
                head = tree.find('head')
                # if this is false the content is malformed, skip it
                if len(head):
                    # create the freshen script element
                    freshen_script = etree.SubElement(head, 'script', type='text/javascript', charset='utf-8', src='http://localhost:9020/freshen.js')

                    response.content = html.tostring(tree, pretty_print=True)
        except:
            pass

        return response
