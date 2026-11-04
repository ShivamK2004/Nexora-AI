import urllib.request, json, sys
url=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8000')+'/api/health'
with urllib.request.urlopen(url,timeout=5) as response:
    data=json.loads(response.read().decode())
print(data)
