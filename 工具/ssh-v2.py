#coding=utf8
__author__ = 'Perling'

import paramiko

def con_and_exec(ip,cmd):
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
    channel.send(ip + '\n')

    while not buff.find('[root@'):
        resp = channel.recv(9999)
        print "----" + resp
        buff += resp
    channel.send(cmd)
    try:
        while buff.find('[root@')==-1:
          resp = channel.recv(9999)
          buff += resp
    except Exception, e:
        print "error info:" + str(e)

    print buff
    channel.close()


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('10.2.32.21',22, username='zhaozhilin', password='YsKTcEL!rd7H@B5', timeout=4)


hosts_ip = [
    '11.1.1.66',
    '11.1.1.99',
]
cmd = 'ifocnfig\n'

for host in hosts_ip:
    con_and_exec(host,'cmd')


client.close()

