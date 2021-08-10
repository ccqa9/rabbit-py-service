import json
from optparse import OptionParser

import logger
from model import publisher, consumer

def main():
    log = logger.Logging().logger()

    with open(config_path(log), "r") as f:
        config = json.load(f)

    publisher_config = config["publisher"]
    publisher_client = publisher.Publisher(
        url=publisher_config["url"],
        name=publisher_config["name"],
        exchange_type=publisher_config["exchange_type"],
        delivery_mode=publisher_config["delivery_mode"],
        durable=publisher_config["durable"],
        logger=log
        ) 

    consumer_config = config["consumer"]
    consumer_client = consumer.Consumer(
        url=consumer_config["url"],
        exchange_name=consumer_config["exchange_name"],
        queue_name=consumer_config["queue_name"],
        routing_key=consumer_config["routing_key"],
        arguments=consumer_config["arguments"],
        logger=log
    )
    try:
        publisher_client.connect()
        consumer_client.run()
    except KeyboardInterrupt:
        publisher_client.close()
        consumer_client.stop()        

def config_path(log):
    parser = OptionParser()
    parser.add_option("-c", "--conf", dest="configPath",
                      help="Pass config path", metavar="FILE")
    (options, args) = parser.parse_args()

    config_path = options.configPath

    if None == config_path:
        log.info('No config specified. Using the default config.')
        config_path = 'resources/test_config.json'

    return config_path

if __name__ == '__main__':
    main()