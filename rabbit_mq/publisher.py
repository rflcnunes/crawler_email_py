import pika


class Publisher:
    def __init__(self, host, queue: str, message: str, exchange: str = ''):
        self.host = host
        self.queue = queue
        self.exchange = exchange
        self.message = message

    def publish(self):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            channel = connection.channel()
            channel.queue_declare(queue=self.queue)
            channel.basic_publish(exchange=self.exchange, routing_key=self.queue, body=self.message)
            connection.close()

            print(f" [x] Sent {self.message}")
        except Exception as exception:
            print(f' [ ] Exception: {exception}')
