#!/usr/bin/env python
import pika
import sys
import meteo_utils

import pickle
import datetime

# Establecer Conexión
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='meteo')

#Objeto MeteoDataDetector
air = meteo_utils.MeteoDataDetector()

#Datos polución
meteo_data = air.analyze_pollution()

#Guardar datos de meteo_data en variables
tipo = "pollution"
co2 = meteo_data.get('co2')
time = datetime.datetime.now()
time = time.strftime("%Y-%m-%d %H:%M:%S")

#Construir objeto RawPollutionData
raw_meteo_data = meteo_utils.RawPollutionData(tipo, co2, time)

message = pickle.dumps(raw_meteo_data)

channel.basic_publish(exchange='',
                      routing_key='meteo',
                      body= message)

print(" [x] Sent. Type: %s, CO2: %s, Time: %s" % (raw_meteo_data.tipo, raw_meteo_data.co2, raw_meteo_data.time))

connection.close()