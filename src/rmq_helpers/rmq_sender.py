import pika

from constants import RMQ_ADDR, RMQ_PORT
from models.rmq_events import RMQEvent

def send_to_rmq(event: RMQEvent, data: str):
    """
    Sends a message to a RabbitMQ exchange with a specific routing key derived from an RMQEvent.

    Args:
        event (RMQEvent): The event type that determines the routing key.
        data (str): The message data to be sent.

    Description:
        This function establishes a connection to RabbitMQ, declares a topic exchange if not already declared,
        and sends a message to it. It is used to communicate events and associated data through RabbitMQ.
    """
    connection = None
    try:
        # Establish a new connection to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(RMQ_ADDR, port=RMQ_PORT))
        # Create a new channel on this connection
        channel = connection.channel()

        # Declare a topic exchange named 'main' if it doesn't already exist
        channel.exchange_declare(exchange='main', exchange_type='topic')

        # Publish the message with the routing key derived from the event type
        channel.basic_publish(exchange='main', routing_key=event.name, body=data)
        print(f"Sent {event.name} message: {data}")

    except Exception as e:
        # Handle any exceptions that occur during message publication
        print("Error:", e)
    finally:
        # Ensure the connection is closed properly
        if connection:
            connection.close()
