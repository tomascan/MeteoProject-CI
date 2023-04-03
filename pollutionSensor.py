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


class RawMeteoData:
      def __init__(self, tipo, co2, time):
         self.tipo = tipo
         self.co2 = co2
         self.time = time



#RAW_METEO_DATA
air = meteo_utils.MeteoDataDetector()
meteo_data = air.analyze_pollution()

tipo = "pollution"
co2 = meteo_data.get('co2')
time = datetime.datetime.now()
time = time.strftime("%Y-%m-%d %H:%M:%S")

raw_meteo_data = RawMeteoData(tipo, co2, time)

message = pickle.dumps(raw_meteo_data)

channel.basic_publish(exchange='',
                      routing_key='meteo',
                      body= message)

print(" [x] Sent %r" % str(raw_meteo_data))

connection.close()