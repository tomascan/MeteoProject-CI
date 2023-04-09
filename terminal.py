import pika
import sys, os
import pickle
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Inicializar datos
wellness_data = []
pollution_data = []
time_data = []

# Crear gráfico
fig, axs = plt.subplots()


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='average', exchange_type='fanout')
    # Crear cola temporal y conectarla al exchange
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='average', queue=queue_name)

    # Definir Callback
    def callback(ch, method, properties, body):
        data = pickle.loads(body)
        print(f"Recibido: {data}")

        # Obtener los valores de la respuesta
        wellness = data.get('wellness', {}).get('value')
        pollution = data.get('pollution', {}).get('value')
        time = data.get('wellness', {}).get('time')

        # Agregar los valores a las listas
        wellness_data.append(wellness)
        pollution_data.append(pollution)
        time_data.append(time)

        # Actualizar el gráfico
        axs.clear()
        axs.plot_date(time_data, wellness_data, '-b', label='Wellness')
        axs.plot_date(time_data, pollution_data, 'r', label='Pollution')
        axs.set_title('Wellness and Pollution')
        axs.legend()
        axs.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.pause(0.01)

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