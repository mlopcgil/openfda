import http.server
import http.client
import json
import socketserver

PORT=8000

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
#class hereda los métodos de BaseHTTPRequestHandler


    def pagina(self): #creamos la página principal
        html = """
            <html>
                <head>
                    <title>OpenFDA App</title>
                </head>
                <body style='background-color: pink'>
                    <h1>OpenFDA Client </h1>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Drug List">
                        </input>
                    </form>
                    
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Company List">
                        </input>
                    </form>
                    
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Company Search">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Warnings List">
                        </input>
                    </form>
                </body>
            </html>
                """
        return html
    def web (self, lista):
        html_lista = """
                                <html>
                                    <head>
                                        <title>OpenFDA Cool App</title>
                                    </head>
                                    <body style='background-color: pink'>
                                        <ul>
                            """
        for i in lista:
            html_lista += "<li>" + i + "</li>"

        html_lista += """
                                        </ul>
                                    </body>
                                </html>
                            """
        return html_lista
    def datos (self, limit=10):
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", "/drug/label.json" + "?limit="+str(limit))
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        dato_general = r1.read().decode("utf8")
        dato_definitivo = json.loads(dato_general)
        resultados = dato_definitivo['results']
        return resultados
    def do_GET(self):
        tecnica = self.path.split("?")
        if len(tecnica) > 1:
            parametros = tecnica[1]
        else:
            parametros = ""

        limit = 1

        if parametros:
            estudio_limit = parametros.split("=")
            if estudio_limit[0] == "limit":
                limit = int(estudio_limit[1])
                print("Limit: {}".format(limit))
        else:
            print("SIN PARAMETROS")




        if self.path=='/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html=self.pagina()
            self.wfile.write(bytes(html, "utf8"))
        elif 'listDrugs' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            drugs = []
            resultados = self.datos(limit)
            for resultado in resultados:
                if ('generic_name' in resultado['openfda']):
                    drugs.append (resultado['openfda']['generic_name'][0])
                else:
                    drugs.append('Desconocido')
            html = self.web (drugs)
            self.wfile.write(bytes(html, "utf8"))
        elif 'listCompanies' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            companies = []
            resultados = self.datos (limit)
            for resultado in resultados:
                if ('manufacturer_name' in resultado['openfda']):
                    companies.append (resultado['openfda']['manufacturer_name'][0])
                else:
                    companies.append('Desconocido')
            html = self.web(companies)
            self.wfile.write(bytes(html, "utf8"))
        elif 'listWarnings' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            warnings = []
            resultados = self.datos (limit)
            for resultado in resultados:
                if ('warnings' in resultado):
                    warnings.append (resultado['warnings'][0])
                else:
                    warnings.append('Desconocido')
            html = self.web(warnings)
            self.wfile.write(bytes(html, "utf8"))
        elif 'searchDrug' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            limit = 10
            drug=self.path.split('=')[1]
            drugs = []
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json" + "?limit="+str(limit) + '&search=active_ingredient:' + drug)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            dato_general = r1.read().decode("utf8")
            dato_definitivo = json.loads(dato_general)
            search_drug = dato_definitivo['results']
            for resultado in search_drug:
                if ('generic_name' in resultado['openfda']):
                    drugs.append(resultado['openfda']['generic_name'][0])
                else:
                    drugs.append('Desconocido')

            html = self.web(drugs)
            self.wfile.write(bytes(html, "utf8"))
        elif 'searchCompany' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            limit = 10
            company=self.path.split('=')[1]
            companies = []
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json" + "?limit=" + str(limit) + '&search=openfda.manufacturer_name:' + company)
            r1 = conn.getresponse()
            print(r1.status, r1.reason)
            dato_general = r1.read().decode("utf8")
            dato_definitivo = json.loads(dato_general)
            search_company = dato_definitivo['results']

            for resultado in search_company:
                companies.append(resultado['openfda']['manufacturer_name'][0])
            html = self.web(companies)
            self.wfile.write(bytes(html, "utf8"))
        elif 'redirect' in self.path:
            self.send_response(301)
            self.send_header('Location', 'http://localhost:' + str(PORT))
            self.end_headers()
        elif 'secret' in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()
        else:
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(self.path).encode())
        return



socketserver.TCPServer.allow_reuse_address= True #permite que se pueda reutilizar el puerto 8000

Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
#para atender las peticiones







