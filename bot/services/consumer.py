from pika import ConnectionParameters, BlockingConnection
import pika
import json
from services.sender import send_notification
import asyncio
import aio_pika

conn_params = ConnectionParameters(
    host = "localhost",
    port = 5672,
    credentials=pika.PlainCredentials(
        username='rmuser',
        password='123123'
    ),
    client_properties={
        'connection_name':'edunext.notifications'
    }
) 

async def callback(message: aio_pika.IncomingMessage):
    async with message.process():
        print("Received:", message.body.decode())

        data = json.loads(message.body.decode())

        await send_notification(data["message"])

async def create_connection():
    connection = await aio_pika.connect_robust(
        "amqp://rmuser:123123@localhost/",
        client_properties={"connection_name": "async-telegram-bot"}
    )

    # Create a channel
    channel = await connection.channel()

    # Declare the queue
    queue = await channel.declare_queue(
        "telegram-notification-queue",
        durable=True
    )

    # Start listening
    await queue.consume(callback)

    print("Waiting for messages. To exit, press Ctrl+C")
    try:
        await asyncio.Future()  # Run forever
    finally:
        await connection.close()