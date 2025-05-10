import urllib.request
from bs4 import BeautifulSoup
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "http://py4e-data.dr-chuck.net/comments_2213416.html"

html = urllib.request.urlopen(url, context=ctx).read()

soup = BeautifulSoup(html, 'html.parser')

#total = 0
tags = soup('span')
#for tag in tags:
#    total = total + int(tag.contents[0])
#print(total)

total = 0
for tag in tags:
    total += int(tag.text)

print(total)