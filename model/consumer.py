import pika

class Consumer(object):

    def __init__(self, url, exchange_name, queue_name, routing_key, arguments, logger):
        self.url = url
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.arguments = arguments
        self.connection = None
        self.channel = None 
        self.log = logger

    def connect(self):
        connection_params = None
        if self.url is 'localhost':
            connection_params = pika.URLParameters(self._url)
        else:
            connection_params = pika.ConnectionParameters(self.url)  

        self.connection = pika.SelectConnection(
            parameters=connection_params,
            on_open_callback=self.on_connection_open)

        return self.connection
        
    def on_connection_open(self):
        self.log.info('Connection opend {}'.format(self.exchange_name))
        self.open_channel()


    def open_channel(self):
        self.log.info('Creating a channel {}'.format(self.exchange_name))
        self.channel = self.connection.channel()


    def setup_queue(self):
        self.log.info('Declaring a queue {}'.format(self.queue_name))
        self.channel.queue_declare(
            callback=self.on_queue_declare,
            queue=self.queue_name,
            arguments=self.arguments)
    

    def on_queue_declare(self):
        self.log.info('A queue is declared {}'.format(self.queue_name))
        self.bind_queue()

    def bind_queue(self):
        self.log.info('Binding a queue {} to {} with {}'.format(self.queue_name, self.exchange_name, self.routing_key))
        self.channel.queue_bind(
            callback=self.on_queue_bind,
            queue=self.queue_name,
            exchange=self.exchange_name,
            routing_key=self.routing_key
        )   

    def on_queue_bind(self):
        self.log.info('A queue is binded {} to {} with {}'.format(self.queue_name, self.exchange_name, self.routing_key))    
        self.start_consuming()

    def start_consuming(self):
        self.log.info('Start consuming for {}'.format(self.queue_name))
        self.channel.basic_consume(
            queue=self.queue_name,
            callback=self.on_message
        )

    def on_message(self, channel, method, header, body):
        self.log.info('A message consuming {}'.format(body))


    def stop_consuming(self):
        if self.channel is not None:
            self.channel.basic_cancel(callback=self.on_cancel)

    def on_cancel(self):
        self.channel.close() 


    def run(self):
        self.connection = self.connect()
        self.connection.ioloop.start()

    def stop(self):
        self.stop_consuming()
        self.connection.ioloop.stop()    