import re
import random
import urllib2
import urllib
import json
import cookielib
import time
import ssl

def wso2_store_login():
    url = 'http://54.222.138.103:9763/store/apis/user/login'
    values = {'username': 'admin', 'password': 'admin'}
    postData = json.dumps(values)
    cookieJar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    req = urllib2.Request(url, postData)
    req.add_header("Content-Type","application/json")
    resp = opener.open(req)
    print "login log:" + resp.read()
    return opener


def get_my_subs():
    opener = wso2_store_login()
    url = 'https://54.222.138.103:9443/store/extensions/assets/webapp/subscriptions'
    ssl._create_default_https_context = ssl._create_unverified_context
    req = urllib2.Request(url)
    resp = opener.open(req)
    m = re.findall(r'<div class="span3 asset store-my-item" >([\s\S]*?<strong>.*?</strong>)',resp.read())
    if m:
        print m
        for i in m:
            print '------------------------'
            print i
            print '------------------------'
            # n = re.match(r'[\s\S]*a href="(.*?)"[\s\S]*href="/store/assets/webapp/(.*?)[\s\S]*<strong>(.*)</strong>[\s\S]*"',i)
            n = re.match(r'[\s\S]*a href="(.*?)"[\s\S]*href="/store/assets/webapp/(.*?)"[\s\S]*<strong>(.*)</strong>[\s\S]*',i)
            if n:
                print "********************************************"
                sub_info = {}
                sub_info['uuid'] = n.group(2)
                sub_info['app_name'] = n.group(3)
                sub_info['href'] = n.group(1)
                print sub_info

#print wso2_store_login()
print get_my_subs()



