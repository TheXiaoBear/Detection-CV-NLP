import pika
from infra.nacos.settings import settings


def get_connection():

    # credentials = pika.PlainCredentials(
    #     "admin",
    #     "123456789"
    # )
    #
    # connection = pika.BlockingConnection(
    #     pika.ConnectionParameters(
    #         host="192.168.233.135",
    #         port=5672,
    #         credentials=credentials
    #     )
    # )

    credentials = pika.PlainCredentials(
        settings.MQ_USERNAME,
        settings.MQ_PASSWORD
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.MQ_HOST,
            port=settings.MQ_PORT,
            credentials=credentials
        )
    )

    return connection