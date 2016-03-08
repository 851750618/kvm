# coding=utf8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, models
from django.contrib import messages
import re
import random
import urllib2
import urllib
import json
import cookielib
import time
import ssl
import MySQLdb

domain = 'http://127.0.0.1:8000/'
wso2_server = '54.222.138.103'
wso2_database_server = '54.222.138.103'
wso2_database_user = 'root'
wso2_database_pass = '123456'

def get_loginuser_role(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    userrole_str = request.session.get('userrole')
    roles = []
    for i in str(userrole_str).split('_'):
        if i == '1':
            roles.append('User')
        elif i == '2':
            roles.append('Creator')
        elif i == '3':
            roles.append('Publisher')
        elif i == '4':
            roles.append('Admin')
    return roles

def wso2_login():
    url = 'http://' + wso2_server + ':9763/publisher/api/authenticate'
    values = {'action': 'login', 'username': 'admin', 'password': 'admin'}
    postData = urllib.urlencode(values)
    cookieJar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    req = urllib2.Request(url, postData)
    resp = opener.open(req)
    print "login log:" + resp.read()
    return opener

def get_webapp_list(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    if request.GET.has_key('show_in_review_only'):
        show_in_review_only = request.GET['show_in_review_only']
    else:
        show_in_review_only = 'off'
    if request.GET.has_key('not_return_request'):
        not_return_request = request.GET['not_return_request']
    else:
        not_return_request = 'off'
    url = 'http://' + wso2_server + ':9763/publisher/assets/webapp/'
    req = urllib2.Request(url)
    opener = wso2_login()
    resp = opener.open(req)
    return_str = resp.read()
    m = re.findall(r'<tr>([\s\S]*?)</tr>',return_str)
    if m:
        all_web_app_info = []
        for i in m:
            tmp_str = ''
            for i in i.split('\n'):
                tmp_str = tmp_str + i
            n = re.match(r'.*?href.*?>\s+(.*?)\s+</a>\s+</td>\s+<td>\s+(.*?)\s+</td>\s+<td>\s+(.*?)\s+</td>.*?<small>(.*?)</small>.*?<small><i class=.*?</i> (.*?)</small></span>.*data-app-id="(.*?)".*" /.*',tmp_str)
            if n:
                if show_in_review_only == 'on' and n.group(5) != 'In-Review':
                    continue
                if not_return_request == 'on' and n.group(5) != 'Published':
                    continue
                app_info = {
                    'name' : n.group(1),
                    'version' : n.group(2),
                    'owner' : n.group(3),
                    'create_time' : n.group(4),
                    'status' : n.group(5),
                    'uuid' : n.group(6)
                }
                all_web_app_info.append(app_info)
    else:
        all_web_app_info = []
    if not_return_request == 'on':
        return all_web_app_info
    username = request.session.get('username')
    current_role = request.session.get('current_role')
    roles = get_loginuser_role(request)
    return render(request,'webapp_list.html',{'login_user':username,'roles':roles,'current_role':current_role,'all_web_app_info':all_web_app_info,'show_in_review_only':show_in_review_only})

def create_web_app(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    username = request.session.get('username')
    current_role = request.session.get('current_role')
    roles = get_loginuser_role(request)
    return render(request,'webapp_list.html',{'login_user':username,'roles':roles,'current_role':current_role,'show_type':'create_web_app'})

def create_web_app_old(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    overview_name = request.POST['name']
    overview_displayName = request.POST['display_name']
    overview_context = request.POST['context']
    overview_version = request.POST['version']
    overview_transports = request.POST['transports']
    overview_webAppUrl = request.POST['webappurl']
    random_int = random.randint(6062992175668489, 6162992175668489)
    overview_trackingCode = 'AM_' + str(random_int)
    values = {
        "overview_provider": "admin",
        "overview_name": overview_name,
        "overview_displayName": overview_displayName,
        "overview_context": overview_context,
        "overview_version": overview_version,
        "optradio": "on",
        "overview_transports": overview_transports,
        "overview_webAppUrl": overview_webAppUrl,
        "overview_description": "",
        "images_thumbnail": "",
        "images_banner": "",
        "context": "",
        "version": "",
        "overview_tier": "Unlimited",
        "overview_trackingCode": overview_trackingCode,
        "tags": "",
        "overview_allowAnonymous": "false",
        "overview_skipGateway": "false",
        "roles": "",
        "overview_logoutUrl": "",
        "uritemplate_policyGroupIds": "[6]",
        "uritemplate_policyPartialIdstemp": "[]",
        "uritemplate_javaPolicyIds": "[5]",
        "uritemplate_urlPattern4": "/*",
        "uritemplate_httpVerb4": "OPTIONS",
        "uritemplate_policyGroupId4": "6",
        "uritemplate_urlPattern3": "/*",
        "uritemplate_httpVerb3": "DELETE",
        "uritemplate_policyGroupId3": "6",
        "uritemplate_urlPattern2": "/*",
        "uritemplate_httpVerb2": "PUT",
        "uritemplate_policyGroupId2": "6",
        "uritemplate_urlPattern1": "/*",
        "uritemplate_httpVerb1": "POST",
        "uritemplate_policyGroupId1": "6",
        "uritemplate_urlPattern0": "/*",
        "uritemplate_httpVerb0": "GET",
        "uritemplate_policyGroupId0": "6",
        "entitlementPolicies": "",
        "autoConfig": "on",
        "providers": "wso2is-5.0.0",
        # "sso_ssoProvider": "wso2is-5.0.0",
        "claims": "http://wso2.org/claims/otherphone",
        "claimPropertyCounter": "1",
        "claimPropertyName0": "http://wso2.org/claims/role",
        "sso_singleSignOn": "Enabled",
        "sso_idpProviderUrl": "https://localhost:9444/samlsso/",
        "sso_saml2SsoIssuer": "",
        "oauthapis_apiName1": "",
        "oauthapis_apiConsumerKey1": "",
        "oauthapis_apiConsumerSecret1": "",
        "oauthapis_apiTokenEndpoint1": "",
        "oauthapis_apiName2": "",
        "oauthapis_apiConsumerKey2": "",
        "oauthapis_apiConsumerSecret2": "",
        "oauthapis_apiTokenEndpoint2": "",
        "oauthapis_apiName3": "",
        "oauthapis_apiConsumerKey3": "",
        "oauthapis_apiConsumerSecret3": "",
        "oauthapis_apiTokenEndpoint3": "",
        "webapp": "webapp",
    }
    parm = urllib.urlencode(values)
    url = 'http://' + wso2_server + ':9763/publisher/asset/webapp'
    req = urllib2.Request(url, parm)
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    opener = wso2_login()
    try:
        resp = opener.open(req)
        re = resp.read()
        print "id-------" + re
        # return  HttpResponse(re)
    except urllib2.URLError, e:
        print e.reason

    print "------------------------"
    time.sleep(2)
    return HttpResponseRedirect(domain + 'wso2/index/')

def delete_web_app(request):
    return 'a'

def change_life_cycle(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    lifecycle_state_to_be_changed = request.GET['lifecycle_state_to_be_changed']
    if lifecycle_state_to_be_changed == 'Submit for Review':
        lifecycle_state_to_be_changed = 'Submit%20for%20Review'
    application_id = request.GET['application_id']
    if lifecycle_state_to_be_changed == 'delete':
        url = 'http://' + wso2_server + ':9763/publisher/api/asset/delete/webapp/' + application_id
        print url
        req = urllib2.Request(url)
        req.get_method = lambda: 'POST'
        opener = wso2_login()
        try:
            resp = opener.open(req)
            print resp.read()
        except urllib2.URLError, e:
            print e.reason
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    url = "http://" + wso2_server + ":9763/publisher/api/lifecycle/" + lifecycle_state_to_be_changed + "/webapp/" + application_id
    print url
    req = urllib2.Request(url)
    req.get_method = lambda: 'PUT'
    opener = wso2_login()
    try:
        resp = opener.open(req)
        print resp.read()
    except urllib2.URLError, e:
        print e.reason
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def wso2_store_login():
    url = 'http://' + wso2_server + ':9763/store/apis/user/login'
    values = {'username': 'admin', 'password': 'admin'}
    postData = json.dumps(values)
    cookieJar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    req = urllib2.Request(url, postData)
    req.add_header("Content-Type","application/json")
    resp = opener.open(req)
    print "login log:" + resp.read()
    return opener

def get_my_subs_old(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    opener = wso2_store_login()
    url = 'https://' + wso2_server + ':9443/store/extensions/assets/webapp/subscriptions'
    ssl._create_default_https_context = ssl._create_unverified_context
    req = urllib2.Request(url)
    resp = opener.open(req)
    m = re.findall(r'<a href="/store/assets/webapp/(.*)"><h4>(.*)</h4></a>',resp.read())
    all_sub_info = []
    if m:
        for i in m:
            sub_info = {}
            sub_info['uuid'] = i[0]
            sub_info['app_name'] = i[1]
            all_sub_info.append(sub_info)
    username = request.session.get('username')
    current_role = request.session.get('current_role')
    roles = get_loginuser_role(request)
    return render(request,'webapp_sub.html',{'login_user':username,'roles':roles,'current_role':current_role,'all_sub_info':all_sub_info})


def get_my_subs_old_v2(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    opener = wso2_store_login()
    url = 'https://' + wso2_server + ':9443/store/extensions/assets/webapp/subscriptions'
    ssl._create_default_https_context = ssl._create_unverified_context
    req = urllib2.Request(url)
    try:
        resp = opener.open(req)
    except urllib2.URLError, e:
        y = re.match(r'.*Internal Server Error.*',e.reason)
        if y:
            print "error,logout and re-login"
            wso2_login()
            get_webapp_list(request)
            resp = opener.open(req)
    m = re.findall(r'<div class="span3 asset store-my-item" >([\s\S]*?<strong>.*?</strong>)',resp.read())
    all_sub_info = []
    if m:
        for i in m:
            n = re.match(r'[\s\S]*a href="(.*?)"[\s\S]*href="/store/assets/webapp/(.*?)"[\s\S]*<strong>(.*)</strong>[\s\S]*',i)
            sub_info = {}
            sub_info['uuid'] = n.group(2)
            sub_info['app_name'] = n.group(3)
            sub_info['href'] = re.subn(r'192\.168\.122\.1','54.222.138.103',n.group(1))[0]
            all_sub_info.append(sub_info)
    username = request.session.get('username')
    current_role = request.session.get('current_role')
    roles = get_loginuser_role(request)
    return render(request,'webapp_sub.html',{'login_user':username,'roles':roles,'current_role':current_role,'all_sub_info':all_sub_info})

def get_my_subs(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    all_sub_info = []
    username = request.session.get('username')
    current_role = request.session.get('current_role')
    roles = get_loginuser_role(request)
    try:
        conn = MySQLdb.connect(host=wso2_database_server,user=wso2_database_user,passwd=wso2_database_pass,port=3306)
        conn.select_db('WSO2AM_DB')
        cur = conn.cursor()
        sql = "SELECT * FROM APM_SUBSCRIPTION where APPLICATION_ID = 2"
        cur.execute(sql)
        results = cur.fetchall()
        fetch_app_id = []
        for row in results:
            fetch_app_id.append(row[3])
        cur.close()
        cur = conn.cursor()
        for app_id in fetch_app_id:
            sub_info = {}
            sql = "SELECT * FROM APM_APP where APP_ID = %d"%(app_id)
            cur.execute(sql)
            results = cur.fetchall()
            sub_info['uuid'] = results[0][7]
            sub_info['app_name'] = results[0][3]
            sub_info['href'] = 'http://%s:8280%s/%s/'%(wso2_server,results[0][5],results[0][4])
            all_sub_info.append(sub_info)
        conn.close()
        return render(request,'webapp_sub.html',{'login_user':username,'roles':roles,'current_role':current_role,'all_sub_info':all_sub_info})
    except MySQLdb.Error,msg:
        print "MySQL Error %d: %s" %(msg.args[0],msg.args[1])
    return HttpResponse('a')


def get_all_published(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    all_pub = get_webapp_list(request)
    username = request.session.get('username')
    current_role = request.session.get('current_role')
    roles = get_loginuser_role(request)
    return render(request,'webapp_all_sub.html',{'login_user':username,'roles':roles,'current_role':current_role,'all_pub':all_pub})


def sub_one_webapp(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    if request.GET['action'] == 'get_details':
        webapp_details = {}
        webapp_details['name'] = request.GET['name']
        webapp_details['uuid'] = request.GET['uuid']
        webapp_details['version'] = request.GET['version']
        webapp_details['time'] = request.GET['time']
        webapp_details['provider'] = request.GET['provider']
        webapp_details['status'] = request.GET['status']
        try:
            conn = MySQLdb.connect(host=wso2_database_server,user=wso2_database_user,passwd=wso2_database_pass,port=3306)
            conn.select_db('WSO2AM_DB')
            cur = conn.cursor()
            sql = "SELECT APP_ID FROM APM_APP WHERE APP_NAME = '%s' AND APP_VERSION = '%s'"%(webapp_details['name'],webapp_details['version'])
            print sql
            cur.execute(sql)
            results = cur.fetchall()
            sub_app_id = results[0][0]
            sql = "SELECT * FROM APM_SUBSCRIPTION WHERE APP_ID = %s"%(sub_app_id)
            cur.execute(sql)
            results = cur.fetchall()
            print results
            if len(results) >= 1:
                webapp_details['is_or_sub'] = 'is'
            else:
                webapp_details['is_or_not_sub'] = 'not'
            cur.close()
            conn.close()
        except MySQLdb.Error,msg:
            print "MySQL Error %d: %s" %(msg.args[0],msg.args[1])
        opener = wso2_login()
        url = 'http://' + wso2_server + ':9763/publisher/api/asset/webapp/' + webapp_details['uuid']
        req = urllib2.Request(url)
        resp = opener.open(req)
        de_json = json.loads(resp.read())
        context = 'http://' + wso2_server + ':8280' + de_json['attributes']['overview_context'] + '/' + request.GET['version']
        webapp_details['context'] = context
        username = request.session.get('username')
        current_role = request.session.get('current_role')
        roles = get_loginuser_role(request)
        return render(request,'webapp_details.html',{'login_user':username,'roles':roles,'current_role':current_role,'webapp_details':webapp_details})
    elif request.GET['action'] == 'sub':
        apiName = request.GET['appname']
        apiVersion = request.GET['appversion']
        try:
            conn = MySQLdb.connect(host=wso2_database_server,user=wso2_database_user,passwd=wso2_database_pass,port=3306)
            conn.select_db('WSO2AM_DB')
            cur = conn.cursor()
            sql = "SELECT APP_ID FROM APM_APP WHERE APP_NAME = '%s' AND APP_VERSION = '%s'"%(apiName,apiVersion)
            print sql
            cur.execute(sql)
            results = cur.fetchall()
            sub_app_id = results[0][0]
            sql = "INSERT INTO APM_SUBSCRIPTION (SUBSCRIPTION_TYPE,TIER_ID,APP_ID,APPLICATION_ID,SUB_STATUS) VALUES ('INDIVIDUAL','Unlimited',%s,2,'UNBLOCKED')"%(sub_app_id)
            print sql
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        except MySQLdb.Error,msg:
            print "MySQL Error %d: %s" %(msg.args[0],msg.args[1])
    elif request.GET['action'] == 'unsub':
        apiName = request.GET['appname']
        apiVersion = request.GET['appversion']
        try:
            conn = MySQLdb.connect(host=wso2_database_server,user=wso2_database_user,passwd=wso2_database_pass,port=3306)
            conn.select_db('WSO2AM_DB')
            cur = conn.cursor()
            sql = "SELECT APP_ID FROM APM_APP WHERE APP_NAME = '%s' AND APP_VERSION = '%s'"%(apiName,apiVersion)
            print sql
            cur.execute(sql)
            results = cur.fetchall()
            sub_app_id = results[0][0]
            sql = "DELETE FROM APM_SUBSCRIPTION WHERE APP_ID = %s"%(sub_app_id)
            print sql
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        except MySQLdb.Error,msg:
            print "MySQL Error %d: %s" %(msg.args[0],msg.args[1])



