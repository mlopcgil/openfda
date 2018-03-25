import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
#realizamos los mismos pasos que en el programa 1 pero con un cambio
conn.request("GET", "/drug/label.json?limit=10", None, headers)
#como te pide los 10 primeros medicamentos ponemos ?limit=10 en el que solo te aparecerán esos
r1 = conn.getresponse()
print(r1.status, r1.reason)
label_general = r1.read().decode("utf-8")
conn.close()

label_definitiva = json.loads(label_general)
#se vuelve a mejorar el label

for i in range(len(label_definitiva['results'])):
    información_medicamento=label_definitiva['results'][i]
#en vez de crear una lista para cada medicamento creamos un bucle que te recorra todos los medicamentos
#para ello usamos range para establecer el intervalo y len para que sea en esa longitud
#ya no usamos [0] sino [i] que hace referencia a los 10 medicamentos
    print('La id es: ',información_medicamento['id'])


