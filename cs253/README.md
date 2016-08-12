# Udacity: CS253 - Web Development

Intoduction:
------------
This course taught by Steve Hoffman teaches about the basics of Web Development
and building your own blog using Google App Engine

Homework links:
---------------
1. [Practice](http://cs253-first.appspot.com)
2. [1st Homework](http://cs253-homew1.appspot.com)

How to deploy your app?
-----------------------
Once done with building your app and testing it on your sandbox it is time to
deploy your application on the App engine

+ Go to your Google Cloud Platform account console
+ At the menu bar say create project, enter a project-id. This will be chosen
  as the hostname part of your website
+ The next step is to deploy your web app from the terminal
+ To deploy the app, enter the following command. The -V parameter specifies
  a version name of your choice:
  Ex: appcfg.py -A [YOUR\_PROJECT\_ID] -V v1 update ./
+ Your app is now deployed and ready to serve traffic at 
  http://[YOUR\_PROJECT\_ID].appspot.com/.

How to test on your sandbox?
----------------------------
+ Google App Engine SDK has the dev\_appserver.py script that starts a web 
  server at port 8080 on the localhost
+ All testing can be done using the browser pointing at http://localhost:8080
