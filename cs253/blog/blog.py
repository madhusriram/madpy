import os
import webapp2
import jinja2
from time import strftime, localtime
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Post(db.Model, Handler):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateProperty(auto_now_add=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return self.render_str("post.html", p = self)

class PermaLink(Handler):
    """
    Get the latest added blog, use permalink.html as the template
    """
    def get(self, post_id):
        """ 
        param: post_id is the matched integer 
        """
        post = Post.get_by_id(int(post_id))
        
        if not post:
            self.error(404)
            return

        self.render('permalink.html', post = post)

class NewBlog(Handler):
    """
    Get a new blog
    """
    def get(self):
        self.render('newpost.html')

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            a = Post(subject = subject, content = content)
            a.put()
            # Redirect to the permalink page containing the newly added blog
            self.redirect('/blog/%s' %str(a.key().id()))
        else:
            error = 'Please add subject and the blog.'
            self.render('newpost.html',subject = subject, content = content, error = error)

class MainPage(Handler):
    """
    Shows all the blogs 
    """
    def get(self):
        posts = db.GqlQuery('SELECT * from Post order by created DESC limit 10')
        self.render('main.html', posts = posts)
     
app = webapp2.WSGIApplication([('/blog', MainPage), 
                               ('/blog/newpost', NewBlog), 
                               ('/blog/(\d+)', PermaLink)], debug=True)
