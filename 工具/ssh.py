#coding=utf8
__author__ = 'Perling'

import paramiko


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('10.2.32.21',22, username='zhaozhilin', password='YsKTcEL!rd7H@B5', timeout=4)

channel=client.invoke_shell()
channel.settimeout(10)
buff=''
input_id_info = 'see the help information ): '
while not buff.endswith(input_id_info):
    try:
      resp = channel.recv(9999)
    except Exception,e:
      print "error" + str(e)
    buff += resp
    if not buff.find('yes/no')==-1:
      channel.send('yes\n')
      buff=''
channel.send('1\n')


while not buff.find('[root@'):
    resp = channel.recv(9999)
    buff += resp

channel.send('mkdir /tmp/channel\nifconfig\n')
try:
    while buff.find('[root@')==-1:
      resp = channel.recv(9999)
      buff += resp
except Exception, e:
    print "error info:" + str(e)

print buff
channel.close()
client.close()

