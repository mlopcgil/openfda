import http.client
import json

headers = {'User-Agent': 'http-client'} #son las cabeceras de mi petición
#es el cliente de openfda

conn = http.client.HTTPSConnection("api.fda.gov") #creo una conexión
#api.fda es la pagina general donde se pueden encontrar todos los medicamentos
conn.request("GET", "/drug/label.json", None, headers) #a partir de esa conexión se manda una petición
r1 = conn.getresponse() #para conseguir la respuesta
print(r1.status, r1.reason)
label_general = r1.read().decode("utf-8")
conn.close()

label_definitiva = json.loads(label_general)
#arriba se ha importado json
#se modifica label general para que quede mas ordenado
#para ello se usa el json importado con la función loads
#ahora se llama label definitiva con la que se podrá trabajar mejor

información_medicamento=label_definitiva['results'][0]
#con label definitiva se puede ver mejor como esta organizado el archivo
#se puede ver que la información del medicamento está en la carpeta de results


print('La id es: ',información_medicamento['id'])
#para obtener la id cogemos de la información del medicamento la carpeta de la id
#igual con los otros
print('El próposito del producto es: ',información_medicamento['purpose'][0])
print('El nombre del fabricante es: ',información_medicamento['openfda']['manufacturer_name'][0])
