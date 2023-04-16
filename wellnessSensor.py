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


#RAW_METEO_DATA
air = meteo_utils.MeteoDataDetector()
meteo_data = air.analyze_air()

#Obtención de datos 
tipo = "wellness"
temperature = meteo_data.get('temperature')
humidity = meteo_data.get('humidity')
time = datetime.datetime.now()
time = time.strftime("%Y-%m-%d %H:%M:%S")

#Construir objeto RawMeteoData
raw_meteo_data = meteo_utils.RawMeteoData(tipo, temperature, humidity, time) 

#Con diccionario no podemos utilizar MeteoDataProcessor en worker
#raw_meteo_data = {'type': 'wellness','temperature': temperature, 'humidity': humidity, 'time': time}

message = pickle.dumps(raw_meteo_data)

channel.basic_publish(exchange='',
                      routing_key='meteo',
                      body= message)
                      
print(" [x] Sent. Type: %s, Temperature: %s, Humidity: %s, Time: %s" % (raw_meteo_data.tipo, raw_meteo_data.temperature, raw_meteo_data.humidity, raw_meteo_data.time))


connection.close()
