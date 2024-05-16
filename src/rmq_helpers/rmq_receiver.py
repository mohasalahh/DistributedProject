import threading
from typing import List
import pika
import zmq

from models.zeromq_events import ZeroMQEvent

class ZMQEventReceiver(threading.Thread):

    def __init__(self, events: List[ZeroMQEvent], did_receive_function, addr: str = 'tcp://localhost:5555'):
        super().__init__()
        self.events = events
        self.did_receive_function = did_receive_function


    def run(self):
        self.consume_messages(self.events)


    def consume_messages(self, events: List[ZeroMQEvent]):
        # Connect to RabbitMQ server
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        # Create a channel
        channel = connection.channel()

        # Declare a topic exchange named 'main'
        channel.exchange_declare(exchange='main', exchange_type='topic')

        # Declare an exclusive queue (a unique queue for each consumer)
        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

        # Bind the queue to the 'logs' exchange with multiple routing keys
        for event in events:
            channel.queue_bind(exchange='main', queue=queue_name, routing_key=event.name)

        # Start consuming messages from the queue, calling the callback function for each message
        channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=True)

        # Begin consuming messages
        print(f"Waiting for messages: {events}. To exit, press CTRL+C")
        channel.start_consuming()
        
    def callback(self, ch, method, properties, body):
        event_name = method.routing_key
        print("received message->  ", event_name, ": ", body)
        message = body.decode('utf-8')
        if event_name in ZeroMQEvent.__members__:
            message_enum = ZeroMQEvent[event_name]
            self.did_receive_function(message_enum, message)
        else:
            print("Message not found")


