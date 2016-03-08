import MultipartPostHandler, urllib2,json

httpHandler = urllib2.HTTPHandler(debuglevel=1)
opener = urllib2.build_opener(httpHandler)

value = {"categories":["web"]}
post_json = json.dumps(value)

boundary='--AaB03x'
data = []
data.append(boundary)
data.append('content-disposition: form-data; name="import_package_wizard-current_step"')
data.append(boundary)
data.append('Content-Disposition: form-data; name="JsonString"')
data.append('Content-Type: application/json')
data.append(post_json)
data.append(boundary)
data.append('content-disposition: from-data; name="upload-package"; filename="temp_file-83550.zip"')
data.append('Content-Type: application/x-zip-compressed')
data.append('Content-Transfer-Encoding: binary')
data.append(open("D:/Python_file/kvm_upload_package/temp_file-83550.zip","rb").read())
data.append(boundary)

httpBody='\r\n'.join(data)
#print httpBody

req = urllib2.Request('http://54.223.96.127:8082/v1/catalog/package', data=httpBody)
req.add_header("X-Auth-Token", "8921b6caf9354e759201da8497f8bd16")
req.add_header("Content-Type","multipart/form-data; boundary=AaB03x")
req.add_header("Content-Length",len(httpBody))
try:
    opener.open(req)
    print opener.read()
except urllib2.URLError,e:
    print e.reason
    print e.read()

