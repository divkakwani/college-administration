
import os
import webapp2
import jinja2

names_trie = None

# set up jinja2 environment
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
 

class Handler(webapp2.RequestHandler):
    def render_page(self , template , template_values ):
        template = JINJA_ENVIRONMENT.get_template(template)
        self.response.write(template.render(template_values))
        