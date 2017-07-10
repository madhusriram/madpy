# This chapter deals with building a login system
------------------------------------------------

#### Cookies
-------------
- a small (< 4KB) piece of data that is stored in the browser for a website. 
- a cookie is associated with a domain name
- there is a browser limit on how many cookies that can be stored

Cookie's are sent to the browser from a server in the HTTP response header. The respone header might look like this:
. . . . 
. . . . 
Set-cookie: user\_id=12345 (it is of the form name=value)
Set-cookie: user\_id=45678
. . . .

Later HTTP request will send the HTTP request using:
Cookie:user\_id=12345;user\_id=45678

Example: 1
----------
- Connect to google.com using telnet and request their homepage

Maddy-2:Maddy$ telnet google.com 80
Trying 172.217.5.14...
Connected to google.com.
Escape character is '^]'.
GET / HTTP/1.0
Host: www.google.com

HTTP/1.0 200 OK
Date: Thu, 25 Aug 2016 02:00:05 GMT
Expires: -1
Cache-Control: private, max-age=0
Content-Type: text/html; charset=ISO-8859-1
P3P: CP="This is not a P3P policy! See https://www.google.com/support/accounts/answer/151657?hl=en for more info."
Server: gws
X-XSS-Protection: 1; mode=block
X-Frame-Options: SAMEORIGIN
Set-Cookie: NID=85=Kp3ZwsUCM2i0MyJxbakX68IZ7x-Lszb2sD\_1W6rVVwM9nP8gpUeyH0rVu0AFUNPQO0O\_kEnqwFjkcvnJja28sgfUrKTIaDeZ3IVOXX5nFdYBFGnyw2f5Ki1GqTI6HwUtVnliJhNln2rdS-M; expires=Fri, 24-Feb-2017 02:00:05 GMT; path=/; domain=.google.com; HttpOnly

Example: 2
----------
Maddy-2:chap4 Maddy$ curl -I www.google.com
HTTP/1.1 200 OK
Date: Thu, 25 Aug 2016 02:03:30 GMT
Expires: -1
Cache-Control: private, max-age=0
Content-Type: text/html; charset=ISO-8859-1
P3P: CP="This is not a P3P policy! See https://www.google.com/support/accounts/answer/151657?hl=en for more info."
Server: gws
X-XSS-Protection: 1; mode=block
X-Frame-Options: SAMEORIGIN
Set-Cookie: NID=85=kyRmlg-tdLtOCnuqy9BFmnQjRCTf0Fk8Jmkrf17h7gpFDMqWklq0wPNc1Mbvkis0rKFUzix3YHQdBBee\_kMG3hW19LrwYzT6Kn6X3ljrpHGwWmQZM8gj1INEs-j5jlWzHgTwmps3SSi7ohk; expires=Fri, 24-Feb-2017 02:03:30 GMT; path=/; domain=.google.com; HttpOnly
Transfer-Encoding: chunked
Accept-Ranges: none
Vary: Accept-Encoding

Example: 3
----------
Use private browsing in Chrome and use developer tools to monitor the requests and responses

#### Cookie domains
-------------------
Set-Cookie: name=steve; Domain: www.reddit.com; Path=/foo

Path suggests that to what paths the cookie is applied to
Domain parameter suggests what website the cookie is relevant to, in other words the domain parameterrestricts to what domain the cookie will be sent to
The cookie won't get sent to the server if the Domain name name doesn't match the request
The rules for domain matching are:
 - 

Can I have a webserver at reddit.com that'll set a cookie to google.com?
Answer is NO! You may only set cookies to that domain or higher. For example, if the website is www.reddit.com the valid domains are www.reddit.com ; .reddit.com and not bar.reddit.com

#### Rainbow Tables
-------------------
Passwords are hashed, but are they really safe? _NO!!_

Rainbow table: Precomputed hashes 

Note: bcrypt is the best way to hash passwords
