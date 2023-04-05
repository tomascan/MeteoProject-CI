import pika
import sys, os


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='average', exchange_type='fanout')

    # Crear cola temporal y conectarla al exchange
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='average', queue=queue_name)

    # Definir Callback
    def callback(ch, method, properties, body):
        print(f"Recibido: {body}")

    # Consumir mensajes de la cola temporal

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("Waiting for messages...")

    # Iniciar bucle de eventos de RabbitMQ
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

