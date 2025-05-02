import urllib.request
import xml.etree.ElementTree as ET
import ssl

# Ignore SSL certificate errors (useful for https)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Prompt for URL
url = 'http://py4e-data.dr-chuck.net/comments_2213418.xml'

# Read data from URL
data = urllib.request.urlopen(url, context=ctx).read()

# Parse XML data
tree = ET.fromstring(data)

# Find all count elements under comments/comment
counts = tree.findall('.//count')

# Sum all count values
total = sum(int(count.text) for count in counts)

print("Sum:", total)