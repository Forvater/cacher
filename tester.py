import requests

response = ''
try :
    r = requests.get('http://localhost:8000/from_cache?key=123', timeout=1)
    response = r.text
except requests.exceptions.Timeout :
    print 'Connection timeout'
except requests.exceptions.ConnectionError:
    print 'Connection error'
else :
    if response == '' :
        print 'Empty response'
    else:
        print response