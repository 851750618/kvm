import urllib2,json

httpHandler = urllib2.HTTPHandler(debuglevel=1)
opener = urllib2.build_opener(httpHandler)

value = {"categories":["web"]}
post_json = json.dumps(value)

boundary='--AaB03x'
data = []
data.append(boundary)
data.append('content-disposition: form-data; name="submit-name"\r\n')
data.append(boundary)
data.append('Content-Disposition: form-data; name="JsonString"')
data.append('Content-Type: application/json')
data.append(post_json+'\r\n')
data.append(boundary)
data.append('content-disposition: from-data; name="upload-package"; filename="temp_file-83550.zip"')
data.append('Content-Type: application/x-zip-compressed')
data.append('Content-Transfer-Encoding: binary\r\n')
data.append(open("D:/Python_file/kvm_upload_package/temp_file-83550.zip","rb").read())
data.append(boundary)

httpBody='\r\n'.join(data)
#print httpBody

req = urllib2.Request('http://54.223.96.127:8082/v1/catalog/package', data=httpBody)
req.add_header("X-Auth-Token", "efef343a79dc409e9476852ade8489b0")

req.add_header("Content-Type","multipart/form-data; boundary=AaB03x")
req.add_header("Content-Length",len(httpBody))
#httpBody = '"Content-Type":"multipart/form-data; boundary=AaB03x"\r\n' + '"Content-Length":' + str(len(httpBody)) + '\r\n\r\n' + httpBody
try:
    opener.open(req)
    print opener.read()
except urllib2.URLError,e:
    print e.reason
    print e.read()

print httpBody