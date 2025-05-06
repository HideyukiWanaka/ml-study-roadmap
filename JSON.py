import json
import urllib.request
import ssl

# Ignore SSL certificate errors (useful for https)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'http://py4e-data.dr-chuck.net/comments_2213419.json'

data = urllib.request.urlopen(url, context=ctx).read()

info = json.loads(data)

# Extract and sum the 'count' values
sumation = sum(item['count'] for item in info['comments'])

# total = 0
# for item in info['comments']:
#    print(item['count'])
#    print(item['name'])
#    total = total + item['count']

# print("Sum:", total)
print("Sum2:", sumation)
