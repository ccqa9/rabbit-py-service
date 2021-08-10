import pika

class Publisher(object):

    def __init__(self, url, name, exchange_type, durable, delivery_mode, logger):
        self.url = url
        self.name = name
        self.durable = durable
        self.exchange_type = exchange_type
        self.delivery_mode = delivery_mode
        self.connection = None
        self.channel = None 
        self.log = logger

    def connect(self):
        self.log.info('Creating a connection to {}'.format(self.url))
        connection_params = None
        if self.url is 'localhost':
            connection_params = pika.URLParameters(self.url)
        else:
            connection_params = pika.ConnectionParameters(self.url)  

        self.connection = pika.BlockingConnection(connection_params)  
        self.channel = self.connection.channel()  
        self.channel.exchange_declare(exchange=self.name,
                                      exchange_type=self.exchange_type)  


    def send(self, routing_key, message):
        self.log.info('Sending a message {}'.format(message))
        properties=pika.BasicProperties(
                        content_type='text/plain',
                        delivery_mode = self.delivery_mode, # make message persistent
                    )
        self.channel.basic_publish(exchange=self.name,
                                routing_key=routing_key,
                                body=message,
                                properties=properties
                                )      

    def close(self):
        self.connection.close()
        self.log.info('Closed a connection to {}'.format(self.url))                                                          



class Wait:
    def __init__(self, url):
        self.exchange_name = "route.wait"
        self.exchange_
        self._url = url
        self.connection = None
        self.channel = None 