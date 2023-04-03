#!/usr/bin/env python
import pika
import sys
import meteo_utils

# Establecer Conexión
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

air = meteo_utils.MeteoDataDetector()
meteo_data = air.analyze_air()
temperature = meteo_data.get('temperature')
humidity = meteo_data.get('humidity')

print(temperature)
print(humidity)

data = {'temperature': temperature, 'humidity': humidity}

# message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=str(data))

print(" [x] Sent %r" % data)

connection.close()