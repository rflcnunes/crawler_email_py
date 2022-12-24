import pika

try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost'
        ))
    channel = connection.channel()
except Exception as e:
    print(e)


def publish(queue, exchange, routing_key, body):
    try:
        channel.queue_declare(queue=queue)

        channel.basic_publish(exchange=exchange,
                              routing_key=routing_key,
                              body=body)

        print(f" [x] Sent {body}")
        connection.close()
    except Exception as exception:
        print('Exception: ', exception)
