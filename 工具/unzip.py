
import os,zipfile
file_full_path = 'C:\Users\linsm\Desktop\io.murano.apps.apache.ApacheHttpServer.zip'
zfile = zipfile.ZipFile(file_full_path,'r')
for filename in zfile.namelist():
    if filename == 'manifest.yaml':
        data = zfile.read(filename)
        import  yaml
        s = yaml.load(data)
        print s['Description']