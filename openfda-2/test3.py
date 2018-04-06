import http.client
import json

headers = {'User-Agent': 'http-client'}
#Primero hacemos el mismo código que en la otra práctica


conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", '/drug/label.json?limit=100'+'&search=substance_name:"ASPIRIN"', None, headers)
#para buscar todos los productos relacionados con las aspirinas usamos la función search


r1 = conn.getresponse()
print(r1.status, r1.reason)
label_general = r1.read().decode("utf-8")
conn.close()


label_definitiva = json.loads(label_general)

for i in range (len (label_definitiva['results'])):
    información_medicamento=label_definitiva['results'][i]
    print ('La id es: ',información_medicamento['id'])
    if (información_medicamento['openfda']):
        print('El fabricante del producto es: ', información_medicamento['openfda']['manufacturer_name'][0])

