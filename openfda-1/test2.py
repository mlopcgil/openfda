import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
#api.fda es la página general donde se pueden encontrar todos los medicamentos
conn.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
label_general = r1.read().decode("utf-8")
conn.close()

label_definitiva = json.loads(label_general)
for i in range(len(label_definitiva['results'])):
    información_medicamento=label_definitiva['results'][i]
    print('ID: ',información_medicamento['id'])