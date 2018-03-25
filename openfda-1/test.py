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
#para ellos se usa el json importado con la función loads
#ahora se llama label definitiva con la que se podrá trabajar mejor
información_medicamento=label_definitiva['results'][0]
#con la label definitiva se puede ver mejor como está organizado el archivo
#se puede ver que la información del medicamento está en la carpeta de results


print('El id es: ',información_medicamento['id'])
#para obtener los datos de la id, cogemos de la informacion del medicamento la carpeta id
#igual con las otras dos
print('El propósito del producto es: ',información_medicamento['purpose'][0])
print('El nombre del fabricante es: ',información_medicamento['openfda']['manufacturer_name'][0])
