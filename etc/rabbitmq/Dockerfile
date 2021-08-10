FROM rabbitmq:3.8

WORKDIR /

RUN rabbitmq-plugins enable rabbitmq_management
RUN rabbitmq-plugins enable rabbitmq_federation
RUN rabbitmq-plugins enable rabbitmq_federation_management

RUN chmod +x /docker-entrypoint.sh

