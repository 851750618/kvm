import HTMLParser
import re
file = open("C:/Users/linsm/Desktop/apps.html",'r')

content = file.readlines()

m = re.findall(r'<tr>(.*)</tr>',str(content))

for i in m:
    # print i
    n = re.match(r'.*?<a href=\'.*?\'>.*?\s+\'\s+(.*?)\\n.*?</a>.*?</td>.*?<td>\\n.*?(\d.*?)\\n.*?</td>.*?<td>\\n.*?\'\s+(.*?)\\n.*?</td>.*?<small>(.*?)</small>.*<span class="lifecycle-state">.*?</i> (.*?)</small>.*data-app-id=(.*?) />.*',i)
    if n:
        print n.group(1)
        print n.group(2)
        print n.group(3)
        print n.group(4)
        print n.group(5)
        print n.group(6)
    exit(1)