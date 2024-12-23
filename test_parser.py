import requests

url = 'http://localhost:65432/process'
files = {'file': open('/home/oda/consite/consite_server/invoice_parser/tests/inputs/UPSITE-4009.PDF', 'rb')}

response = requests.post(url, files=files)
print(response.text)
