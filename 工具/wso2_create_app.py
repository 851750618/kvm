import re
import random
import urllib2
import urllib
import json
import cookielib
import time

def wso2_login():
    url = 'http://54.222.138.103:9763/publisher/api/authenticate'
    values = {'action': 'login', 'username': 'admin', 'password': 'admin'}
    postData = urllib.urlencode(values)
    cookieJar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    req = urllib2.Request(url, postData)
    resp = opener.open(req)
    print "login log:" + resp.read()
    return opener

def add_policy_group():
    random_int = random.randint(6062992175668489, 7162992175668489)
    policy_group_name = 'De_G_' + str(random_int)
    values = {
        'policyGroupName' : policy_group_name,
        'throttlingTier' : 'Unlimited',
        'userRoles' : '',
        'anonymousAccessToUrlPattern' : 'false',
        'objPartialMappings' : '[]',
        'policyGroupDesc' : 'default policy group for hello world web application'
    }
    parm = urllib.urlencode(values)
    url = ' http://54.222.138.103:9763/publisher/api/entitlement/policy/partial/policyGroup/save'
    req = urllib2.Request(url, parm)
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    opener = wso2_login()
    resp = opener.open(req)
    re = resp.read()
    print re
# print add_policy_group()
# exit(1)
def create_web_app_old():
    overview_name = 'ok_test'
    overview_displayName = 'ok_test'
    overview_context = '/jd'
    overview_version = 'v1'
    overview_transports = 'http'
    overview_webAppUrl = 'http://www.jd.com'
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
    url = 'http://54.222.138.103:9763/publisher/asset/webapp'
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
    exit(1)
    values = {
        "provider": "wso2is-5.0.0",
        "logout_url": "",
        "claims": ["http://wso2.org/claims/role"],
        "app_name": overview_name,
        "app_verison": overview_version,
        "app_transport": overview_transports,
        "app_context": overview_context,
        "app_provider": "admin",
        "app_allowAnonymous": "false"
    }
    parm = json.dumps(values)
    url = 'http://54.222.138.103:9763/publisher/api/sso/addConfig'
    req = urllib2.Request(url, parm)
    req.add_header("X-Auth-Token", "application/json")
    resp = opener.open(req)
    time.sleep(2)
    return '123'

print create_web_app_old()