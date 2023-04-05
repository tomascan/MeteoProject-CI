import redis
import pika
import time
from datetime import datetime, timedelta

# Conexión Redis
r_client = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)

# Conexión RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Crear exchange, recibe mensajes y los distribuye en colas (crear para distintas terminales)
channel.exchange_declare(exchange='average', exchange_type='fanout')

Y = 10

while True:
    # WELLNESS
    w_list = []
    w_string = r_client.lpop("wellness")
    if w_string is None:
        print("No hay datos wellness")
        while True:
            time.sleep(Y)
            w_string = r_client.lpop("wellness")
            if w_string is not None:
                break

    w_first = datetime.strptime(w_string.strip('()').split(" : ")[0], "%Y-%m-%d %H:%M:%S")
    w_limit = w_first + timedelta(seconds=Y)
    w_list.append(float(w_string.strip('()').split(" : ")[1]))
    while True:
        w_string = r_client.lpop("wellness")
        if w_string is None:
            break

        w_time = datetime.strptime(w_string.strip('()').split(" : ")[0], "%Y-%m-%d %H:%M:%S")
        if w_limit < w_time:
            break

        w_list.append(float(w_string.strip('()').split(" : ")[1]))

    w_avg = round(sum(w_list) / len(w_list), 3)

    # POLLUTION
    p_list = []
    p_string = r_client.lpop("pollution")
    if p_string is None:
        print("No hay datos pollution")
        while True:
            time.sleep(Y)
            p_string = r_client.lpop("pollution")
            if p_string is not None:
                break

    p_first = datetime.strptime(p_string.strip('()').split(" : ")[0], "%Y-%m-%d %H:%M:%S")
    p_limit = p_first + timedelta(seconds=Y)
    p_list.append(float(p_string.strip('()').split(" : ")[1]))

    while True:
        p_string = r_client.lpop("pollution")
        if p_string is None:
            break

        p_time = datetime.strptime(p_string.strip('()').split(" : ")[0], "%Y-%m-%d %H:%M:%S")
        if p_limit < p_time:
            break

        p_list.append(float(p_string.strip('()').split(" : ")[1]))

    p_avg = round(sum(p_list) / len(p_list), 3)

    # Publica mensaje en el exchange (Crear para distintas terminales)
    channel.basic_publish(exchange='average', routing_key='',
                          body=f"Wellness: {w_avg}, {w_time}, Pollution: {p_avg}, {p_time}")
    time.sleep(Y)

connection.close()
