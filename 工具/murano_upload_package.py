import urllib2
import json

murano_server = '10.109.253.112'
def send_post(url,parm):
    postData = json.dumps(parm)
    req = urllib2.Request(url, postData)
    req.add_header("Content-Type","application/json")
    resp = urllib2.urlopen(req)
    json_data = json.loads(resp.read())
    return json_data

def getToken():
    values = {"auth": {"tenantName": "admin", "passwordCredentials": {"username": "admin", "password": "123456"}}}
    murano_toekn = send_post("http://" + murano_server + ":5000/v2.0/tokens",values)['access']['token']['id']
    return murano_toekn



boundary='--AaB03x'
data=[]

data.append(boundary)
data.append('content-disposition: form-data; name="submit-name"')
data.append('')
data.append(boundary)
data.append('Content-Disposition: form-data; name="JsonString"')
data.append('Content-Type: application/json')
data.append('{"categories":["web"]')
data.append('')
data.append(boundary)
data.append('content-disposition: file; name="file"; filename="%s"'%('io.murano.apps.ZabbixServer.zip'))
data.append('Content-Type: targz')
data.append('Content-Transfer-Encoding: binary')
data.append('')
file = open(r'C:\Users\linsm\Desktop\io.murano.apps.ZabbixServer.zip','rb')
content = '\n'.join(file.readlines())
file.close()
data.append(content)
data.append(boundary+'--')
httpbody = '\n'.join(data)

print type(httpbody)
print len(httpbody)

req = urllib2.Request('http://' murano_server ':5000/v1/catalog/packages',data=httpbody)
req.add_header('Content-type','multipart/form-data, boundary=AaB03x')
req.add_header('Content-Length',len(httpbody))
req.add_header("X-Auth-Token",getToken())
resp = urllib2.urlopen(req)
print resp.read()