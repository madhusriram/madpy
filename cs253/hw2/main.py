import webapp2
import cgi

error_text = {'error_user' : 'Please enter username',
			  'error_pwd'  : 'Please enter password',
			  'error_pwd2' : 'Passwords mismatch. Try again'}

form="""
<form method="post">
	<label> Username: 
	<input type="text" name="username" value="%s">
	<div style="color: red">%s</div>
	</label>
	<br>
	<label> Password: 
	<input type="password" name="password">
	<div style="color: red">%s</div>
	</label>
	<br>
	<label> Verify Password: 
	<input type="password" name="verify_password">
	<div style="color: red">%s</div>
	</label>
	<br>
	<label> Email(optional): 
	<input type="email" name="email" value="%s">
	</label>
	<br>
	<input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
	def write_form(self, username="", error_user="", error_pwd="",email=""):  
		self.response.out.write(form %(username, error_user, error_pwd, error_pwd, email))

	def get(self):
		self.write_form()
	
	def post(self):
		user = self.request.get('username')
		pwd = self.request.get('password')
		v_pwd = self.request.get('verify_password')
		email = self.request.get('email')
		
		if not (pwd and v_pwd or user):
			self.write_form("", error_text['error_user'],
								error_text['error_pwd'],"")
		# No user name only
		elif not user:
			self.write_form("",error_text['error_user'],"","")
		# No passwords, but there is user or email
		elif not (pwd or v_pwd) and (user or email):
			self.write_form(user,"",error_text['error_pwd'],email)
		elif validate(pwd, v_pwd):
			self.redirect("/welcome/user=" + user) 
		# Validate failed
		else:
			self.write_form(user,"",error_text['error_pwd2'],email)
			

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Welcome to the world of emptiness!")

def validate(password,v_pwd):
	if password == v_pwd:
		return True
	return False

app = webapp2.WSGIApplication([('/', MainPage), ('/welcome', WelcomeHandler)], debug=True)
