import threading
from typing import List
import pika

from constants import RMQ_ADDR, RMQ_PORT
from models.rmq_events import RMQEvent

class RMQEventReceiver(threading.Thread):
    def __init__(self, events: List[RMQEvent], did_receive_function):
        super().__init__()
        self.events = events
        self.did_receive_function = did_receive_function
        self.connection = None
        self.channel = None

    def run(self):
        self.consume_messages(self.events)

    def consume_messages(self, events: List[RMQEvent]):
        try:
            # Establish a new connection
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(RMQ_ADDR, port=RMQ_PORT))
            # Create a new channel
            self.channel = self.connection.channel()

            # Declare a topic exchange named 'main'
            self.channel.exchange_declare(exchange='main', exchange_type='topic')

            # Declare an exclusive queue (a unique queue for each consumer)
            result = self.channel.queue_declare('', exclusive=True)
            queue_name = result.method.queue

            # Bind the queue to the 'logs' exchange with multiple routing keys
            for event in events:
                self.channel.queue_bind(exchange='main', queue=queue_name, routing_key=event.name)

            # Start consuming messages from the queue, calling the callback function for each message
            print(f"Waiting for messages: {events}.")
            self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=True)

            # Begin consuming messages
            self.channel.start_consuming()
        except Exception as e:
            # this will raise an exception when consuming is stopped
            print("ExxxxxError:", e)
        finally:
            # Close the channel and connection when done
            if self.channel and  self.channel.is_open:
                self.channel.close()
            if self.connection and self.connection.is_open:
                self.connection.close()

    def stop_consuming(self):
        if self.channel:
            self.channel.stop_consuming()

    def callback(self, ch, method, properties, body):
        event_name = method.routing_key
        print("received message->  ", event_name, ": ", body)
        message = body.decode('utf-8')
        if event_name in RMQEvent.__members__:
            message_enum = RMQEvent[event_name]
            self.did_receive_function(message_enum, message)
        else:
            print("Message not found")
