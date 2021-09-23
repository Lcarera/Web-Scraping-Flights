import os
# os.system("sudo apt install pip3")
# os.system("pip3 install requests")
# os.system("pip3 install bs4")
# os.system("pip3 install datetime")
#os.system("pip3 install shutil")
import requests as req
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import  ftplib


today = str(datetime.today().strftime('%Y-%m-%d'))

# Clase vuelo, con todos los atributos que se obtienen de la pagina


class Vuelo():

    def __init__(self, airline, code, destiny, time, gate, estatus):
        self.airline = airline
        self.photo = f"https://sjoairport.com/wp-content/themes/aijs-child/images/airlines/{airline.capitalize()}.png"
        self.code = code
        self.destiny = destiny
        self.time = time
        self.date = today
        self.gate = gate[6:].strip()
        self.estados = {
            "A tiempo": 0,
            "Cancelado": 1,
            "Salió": 2,
            "Llegó": 3,
            "Confirmado": 4,
            "Demorado": 5
        }
        self.estatus = estatus
        self.estautus_code = self.estados.get(estatus)


vuelos = []


def find_tags_from_class(html):

    # parse html
    soup = BeautifulSoup(html, "html.parser")

    # Encuentra tags por el nombre de clase
    flights = soup.find_all("div", class_="attribute")
    status = soup.find_all("span", class_="action")

    x = 0
    atributos = []

    estados = []
    # Creando objetos Vuelo, por cada vuelo que se obtenga de la pagina
    for row in status:
        estados.append(row.text.strip())
    for flight in flights:
        if x == 11:
            # Cuando llega a 11 significa que ya almaceno un vuelo entero
            if len(vuelos) > len(estados):
                vuelos.pop(-1)
            if len(vuelos) != 0:
                estado = estados[len(vuelos)-1]
            else:
                estado = estados[0]
            vuelos.append(Vuelo(atributos[0], atributos[1], atributos[2],
                          atributos[3], atributos[4], estado))
            atributos = []
            x = 5
        if x > 5:
            # Almacena los atributos
            x += 1
            atributos.append(flight.text.strip())
        else:
            # Saltea los primeros 5 elementos son lso titulos de la tabla
            x += 1


# Obteniendo HTML
Web = req.get('https://sjoairport.com/flights-new/')
find_tags_from_class(Web.text)

jsonText = {}
jsonText['vuelos'] = []
# Convierte todos los vuelos en formato json
for vuelo in vuelos:
    jsonText['vuelos'].append({

        'aerolinea': vuelo.airline,
        'vuelo': vuelo.code,
        'destino': vuelo.destiny,
        'fecha y hora': f"{vuelo.date} {vuelo.time}",
        'puerta': vuelo.gate,
        'estado': vuelo.estatus,
        'estado_code': vuelo.estautus_code,
        'foto': vuelo.photo,
    })

with open("flights_data.txt", "w") as file:
    json.dump(jsonText, file)
# shutil.move("flights_data.txt",)

time.sleep(900)


# Datos FTP
ftp_servidor = '192.168.255.253'
ftp_usuario  = 'qt1'
ftp_clave    = 'YpMePUXK'
ftp_raiz     = '/Web/Hotel-Telecable/' # donde queremos subir el fichero

# Datos del fichero a subir
fichero_origen = 'flight_data.txt'
fichero_destino = 'flight_data.txt' 

# Conectamos con el servidor
try:
	s = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
	try:
		f = open(fichero_origen, 'rb')
		s.cwd(ftp_raiz)
		s.storbinary('STOR ' + fichero_destino, f)
		f.close()
		s.quit()
	except:
		print( "No se ha podido encontrar el fichero " + fichero_origen)
except:
	print ("No se ha podido conectar al servidor " + ftp_servidor)
