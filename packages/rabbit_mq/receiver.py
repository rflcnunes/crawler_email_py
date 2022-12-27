import pika


class Receiver:
    def __init__(self, queue):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.channel = self.connection.channel()
            self.queue = queue
        except Exception as e:
            print(e)

    @staticmethod
    def callback(self, method, properties, body):
        print(f" [x] Received: {body}")

    def consume(self):
        try:
            self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)

            print(' [*] Waiting for messages. To exit press CTRL+C')
            self.channel.start_consuming()
        except Exception as exception:
            print(' [ ] Exception: ', exception)
