import http.server
import socketserver
import http.client
import json

PORT = 9925
#para lanzar el servidor usamos un puerto


def list():
    lista = []
    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=10", None, headers)

    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    label_general = r1.read().decode("utf-8")
    conn.close()

    label_definitiva = json.loads(label_general)
    for i in range(len(label_definitiva['results'])):
        información_medicamento = label_definitiva['results'][i]
        if (información_medicamento['openfda']):
            print('El medicamento es: ', información_medicamento['openfda']['generic_name'][0])
            lista.append(información_medicamento['openfda']['generic_name'][0])

    return lista

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # handler es un manejador de peticiones
    # class hereda los metodos de BaseHTTPRequestHandler


    def do_GET(self):

        self.send_response(200)
        #para indicar que está bien, ok


        self.send_header('Content-type', 'text/html')
        self.end_headers()
        #para indicar que el contenido será del tipo html
        content="<html><body style='background-color: pink'><h1>Los medicamentos son:</h2>"
        lista=list ()
        for e in lista:
            content += e+"<br>"
            
        content+="</body></html>"

        self.wfile.write(bytes(content, "utf8"))
        return



Handler = testHTTPRequestHandler
#el manejador será la clase

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
#para atender las peticiones del cliente
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Servidor parado")


