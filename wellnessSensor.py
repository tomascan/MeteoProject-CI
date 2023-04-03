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
      def __init__(self, tipo, temperature, humidity, time):
         self.tipo = tipo
         self.temperature = temperature
         self.humidity = humidity
         self.time = time



#RAW_METEO_DATA
air = meteo_utils.MeteoDataDetector()
meteo_data = air.analyze_air()

tipo = "wellness"
temperature = meteo_data.get('temperature')
humidity = meteo_data.get('humidity')
time = datetime.datetime.now()
time = time.strftime("%Y-%m-%d %H:%M:%S")

raw_meteo_data = RawMeteoData(tipo, temperature, humidity, time)


#raw_meteo_data = {'type': 'wellness','temperature': temperature, 'humidity': humidity, 'time': time}

message = pickle.dumps(raw_meteo_data)

channel.basic_publish(exchange='',
                      routing_key='meteo',
                      body= message)

print(" [x] Sent %r" % raw_meteo_data)

connection.close()