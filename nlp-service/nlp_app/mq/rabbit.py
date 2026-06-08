import pika


def get_connection():

    credentials = pika.PlainCredentials(
        "admin",
        "123456789"
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="192.168.233.135",
            port=5672,
            credentials=credentials
        )
    )

    return connection