import http.client
import json

headers = {'User-Agent': 'http-client'}
#Primero hacemos el mismo código que en la otra práctica

skip=0
while True:
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", '/drug/label.json?limit=100&skip='+str(skip)+'&search=substance_name:"ASPIRIN"', None, headers)
    #usamos la función skip porque queremos la información de todos los medicamentos
    #lo pedimos en rodajas de 100
    #el skip sirve para saltarte en el primer caso los 0 primeros, es decir, que no se salte ninguno
    #la siguiente vez que se recorra el bucle se saltará los 100 primeros
    #convertimos en string el skip
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

    if (len(label_definitiva['results'])<100):
        break
        #este if sirve para que si la label tiene menos de 100 el bucle se rompa y no siga
    skip=skip+100
    #se va sumando 100 al skip, por eso en la segunda vuelta se saltaba los 100 primeros