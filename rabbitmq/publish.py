import pika


def publish(queue, message, exchange=''):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_publish(exchange=exchange, routing_key=queue, body=message)
        connection.close()

        print(f" [x] Sent {message}")
    except Exception as exception:
        print(f' [ ] Exception: {exception}')
