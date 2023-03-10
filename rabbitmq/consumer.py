import pika

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
except Exception as e:
    print(e)


def callback(ch, method, properties, body):
    print(f" [x] Received: {body}")


def consume(queue):
    try:
        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except Exception as exception:
        print(' [ ] Exception: ', exception)
