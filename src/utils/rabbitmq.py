import pika
import json
import os

AMQP_URL = os.getenv("AMQP_URL", "amqp://rabbitmq")

def publish_appointment_created(event_data):
    params = pika.URLParameters(AMQP_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='appointments', exchange_type='fanout')
    channel.basic_publish(
        exchange='appointments',
        routing_key='',
        body=json.dumps(event_data)
    )
    print(" [x] Sent AppointmentCreated:", event_data)
    connection.close()
