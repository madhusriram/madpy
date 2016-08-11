import webapp2
import cgi

form="""
	<form method="post">
		<b>Enter some text to ROT13:</b>
		<br>
		<textarea name="text" style="height: 100px; width: 400px;">%s</textarea>
		</br>
		<input type="submit">
	</form>
"""

class MainPage(webapp2.RequestHandler):
	def write_form(self, result=""):
		self.response.out.write(form %result)
		
	def get(self):
		self.write_form()

	def post(self):
		raw_text = self.request.get('text')
		self.write_form(rot13(raw_text))

def rot13(text):
	rot13_str = ''
	for ch in text:
		if ch.isalpha():
			ch = do_rot13(ch)
		rot13_str += str(ch)
	return rot13_str

def do_rot13(ch):
	ascii_ch = ord(ch)
	rot13_ch = ascii_ch + 13

	if ch.islower() and rot13_ch > 122:
		rot13_ch = rot13_ch - 26
	elif ch.isupper() and rot13_ch > 90:
		rot13_ch = rot13_ch - 26
		
	return chr(rot13_ch)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
