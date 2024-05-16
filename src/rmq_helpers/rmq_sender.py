import pika

from models.zeromq_events import ZeroMQEvent

import pika


def send_to_rmq(event: ZeroMQEvent, data: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    # Create a channel
    channel = connection.channel()

    # Declare a topic exchange named 'logs'
    channel.exchange_declare(exchange='main', exchange_type='topic')

    # Publish the message to the 'logs' exchange with the specified routing key
    channel.basic_publish(exchange='main', routing_key=event.name, body=data)
    print(f"Sent {event.name} message: {data}")

    # Close the connection
    connection.close()