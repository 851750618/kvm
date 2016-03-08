#coding=utf8
import urllib2
import urllib
import json
import cookielib
import re
import encodings
import os

url = 'http://54.223.96.224:9763/publisher/api/authenticate'
values = {'action': 'login', 'username': 'admin', 'password': 'admin'}
postData = urllib.urlencode(values)
cookieJar = cookielib.CookieJar()
httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar),httpHandler, httpsHandler)
req = urllib2.Request(url, postData)
resp = opener.open(req)
print "login log:" + resp.read()

url = 'http://54.223.96.224:9763/publisher/api/asset/delete/webapp/ffaf0278-c352-4fa3-aa73-65cf01da0be0'
postData = json.dumps('{"commonAuthId":"7b049b31-32ac-472c-a20e-671b1e3f7753","samlssoTokenId":"d7bbd822-cf6a-446c-a45f-5ec5f739dacc"}')

reqnew = urllib2.Request(url,postData)
reqnew.add_header('Connection','keepalive')
reqnew.add_header('Content-Type','application/json')
resp = opener.open(reqnew)

print resp.read()


