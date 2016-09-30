import requests

r = requests.get('http://localhost:8000/from_cache?key=123', timeout=1)

print r.text

