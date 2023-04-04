import redis
import pika
import time
import pickle

# Conexión Redis
r_client = redis.StrictRedis(host="localhost", port=6379, password="", decode_responses=True)

# Conexión RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Crear exchange
channel.exchange_declare(exchange='average', exchange_type='fanout')

# Obtener listas de redis cada Ys

Y = 30
w_list = []
p_list = []

while True:
    w_string = r_client.rpop("wellness")
    tiempo, wellness = w_string.strip('()').split(" : ")
    print(tiempo, wellness)
    w_list.append(float(wellness))

    p_string = r_client.rpop("pollut")
    tiempo, pollution = p_string.strip('()').split(" : ")
    print(tiempo, pollution)
    p_list.append(float(pollution))

    # Calcular media
    w_avg = sum(w_list) / len(w_list)
    p_avg = sum(p_list) / len(p_list)

    print(f"W avg: {w_avg}")

    print("P avg: {p_avg}")

    # Publish values
    channel.basic_publish(exchange='average', routing_key='', body=f"Wellness: {w_avg}, Pollution: {p_avg}")

    time.sleep(Y)

connection.close()

