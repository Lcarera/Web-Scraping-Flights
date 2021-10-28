import os
import requests as req
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time


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
while True:
	try:
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
	            'hora': vuelo.time,
	            'fecha': vuelo.date,
	            'puerta': vuelo.gate,
	            'estado': vuelo.estatus,
	            'estado_code': vuelo.estautus_code,
	            'foto': vuelo.photo,
	        })

	    vuelos = []
	    with open("flights_data.txt", "w") as file:
	        json.dump(jsonText, file)

	    os.system('chmod a+x ./ftpupload.sh')
	    os.system('./ftpupload.sh')
	    print(datetime)
	except:
	    continue
	finally:
            time.sleep(900)
