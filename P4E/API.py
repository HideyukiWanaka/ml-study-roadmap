import urllib.request
import urllib.parse
import json
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# API endpoint
serviceurl = 'http://py4e-data.dr-chuck.net/opengeo?'

# Prompt for location
address = input('Enter location: ')
params = {'q': address}
url = serviceurl + urllib.parse.urlencode(params)

print('Retrieving', url)
uh = urllib.request.urlopen(url, context=ctx)
data = uh.read().decode()
print('Retrieved', len(data), 'characters')

# Parse JSON
js = json.loads(data)

try:
    plus_code = js['features'][0]['properties']['plus_code']
    print('Plus code:', plus_code)
except:
    print('Plus code not found')
