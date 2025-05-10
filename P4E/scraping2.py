# To run this, download the BeautifulSoup zip file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'http://py4e-data.dr-chuck.net/known_by_Gabriela.html'
count = 7     # Number of times to follow links
position = 18  # Position of the link to follow (1-based)

# ----- Start processing -----
for i in range(count):
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve all anchor tags
    tags = soup('a')

    # Print the name and update the URL
    url = tags[position - 1].get('href', None)
    print(f'Step {i+1}: {tags[position - 1].text}')

print(f'\nLast name in sequence: {tags[position - 1].text}')