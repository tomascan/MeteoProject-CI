#!/usr/bin/env python
import pika, sys, os
import time
import meteo_utils
import pickle
import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""

r_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='meteo')

    def callback(ch, method, properties, body):

        data_queue = pickle.loads(body)

        if data_queue.tipo == 'wellness':
            air_wellness = meteo_utils.MeteoDataProcessor()
            wellness = air_wellness.process_meteo_data(data_queue)
            r_client.rpush('wellness', f'({data_queue.time} : {wellness})')

        else:
            air_pollution = meteo_utils.MeteoDataProcessor()
            pollution = air_pollution.process_pollution_data(data_queue)
            r_client.rpush('pollution', f'({data_queue.time} : {pollution})')

        # time.sleep(body.count(b'.'))
        print(" [x] Done")

    # Añadir al redis

    channel.basic_consume(queue='meteo', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


