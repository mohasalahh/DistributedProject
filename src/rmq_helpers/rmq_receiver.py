import threading
from typing import List
import pika

from constants import RMQ_ADDR, RMQ_PORT
from models.rmq_events import RMQEvent

class RMQEventReceiver(threading.Thread):
    """
    A threaded class for receiving RabbitMQ events. This class handles the connection,
    channel setup, and message consumption for specified RMQ events.

    Attributes:
        events (List[RMQEvent]): List of event types to subscribe to.
        did_receive_function (callable): Function to be called when a message is received.
        connection (pika.BlockingConnection): The RabbitMQ connection.
        channel (pika.Channel): The channel on which to receive messages.
    """
    def __init__(self, events: List[RMQEvent], did_receive_function):
        """
        Initialize the RMQEventReceiver thread with event subscriptions and a callback function.

        Args:
            events (List[RMQEvent]): Events this receiver should listen for.
            did_receive_function (callable): Callback function to handle received messages.
        """
        super().__init__()
        self.events = events
        self.did_receive_function = did_receive_function
        self.connection = None
        self.channel = None

    def run(self):
        """
        Entry point for the thread, starts the message consumption process.
        """
        self.consume_messages(self.events)

    def consume_messages(self, events: List[RMQEvent]):
        """
        Establishes connection to RabbitMQ, sets up the exchange and queue, and begins consuming messages.

        Args:
            events (List[RMQEvent]): A list of events to listen for.
        """
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(RMQ_ADDR, port=RMQ_PORT))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange='main', exchange_type='topic')
            result = self.channel.queue_declare('', exclusive=True)
            queue_name = result.method.queue

            for event in events:
                self.channel.queue_bind(exchange='main', queue=queue_name, routing_key=event.name)

            print(f"Waiting for messages: {events}.")
            self.channel.basic_consume(queue=queue_name, on_message_callback=self.callback, auto_ack=True)
            self.channel.start_consuming()
        except Exception as e:
            print("Error during message consumption:", e)
        finally:
            if self.channel and self.channel.is_open:
                self.channel.close()
            if self.connection and self.connection.is_open:
                self.connection.close()

    def stop_consuming(self):
        """
        Stops the message consuming loop, intended to gracefully shut down message consumption.
        """
        if self.channel:
            self.channel.stop_consuming()

    def callback(self, ch, method, properties, body):
        """
        Callback function triggered by pika when a new message is delivered from the server.

        Args:
            ch (pika.Channel): The channel object.
            method: Method frame with delivery information.
            properties: Properties frame with header information.
            body (bytes): The message body.
        """
        event_name = method.routing_key
        print("Received message -> ", event_name, ": ", body)
        message = body.decode('utf-8')
        if event_name in RMQEvent.__members__:
            message_enum = RMQEvent[event_name]
            self.did_receive_function(message_enum, message)
        else:
            print("Received unrecognized message type")
