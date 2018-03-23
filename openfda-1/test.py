import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
#api.fda es la página general donde se pueden encontrar todos los medicamentos
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
label_general = r1.read().decode("utf-8")
conn.close()

label_definitiva = json.loads(label_general)
información_medicamento=label_definitiva['results'][0]
#la información del medicamento es la label definitiva que hemos creado para mejorar la label general
#y le añadimos results porque es lo que nos interesa


print('ID: ',información_medicamento['id'])
print('Propósito_producto: ',información_medicamento['purpose'][0])
print('Nombre_fabricante: '),información_medicamento[openfda]['manufacturer_name'][0])