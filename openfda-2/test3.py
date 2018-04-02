import http.client
import json

headers = {'User-Agent': 'http-client'}
#Primero hacemos el mismo código que en la otra práctica

skip=0
while True:
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", '/drug/label.json?limit=100&skip='str(skip)+'&search=substance_name:"ASPIRIN"', None, headers)
    #usamos la función skip porque queremos la información de todos los medicamentos
    #creamos un bucle que parte de 0 y que va recorriendo todos los medicamentos
    #convertimos en string el skip
    #para buscar todos los productos relacionados con las aspirinas usamos la función search
    

    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    label_general = r1.read().decode("utf-8")
    conn.close()


    label_definitiva = json.loads(label_general)

    for i in range (len (label_definitiva['results'])):
        información_medicamento=label_definitiva['results'][i]
        print ('La id es: ',medicamento_info['id'])
        print('El fabricante del producto es: ', medicamento_info['openfda']['manufacturer_name'][0])

    if (len(label_definitiva['results'])<100):
        break
    skip=skip+100