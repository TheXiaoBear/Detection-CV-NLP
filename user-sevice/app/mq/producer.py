import json
import pika

from app.mq.rabbit import get_connection


QUEUE_NAME = "cv_queue"


def send_cv_task(task_id: int):

    connection = get_connection()

    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    message = {
        "task_id": task_id
    }

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message)
    )

    connection.close()