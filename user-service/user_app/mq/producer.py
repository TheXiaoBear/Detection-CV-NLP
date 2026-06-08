import json
import pika

from user_app.mq.rabbit import get_connection


QUEUE_NAME = "cv_queue"


def send_cv_task(task_id: int, model_name: str):

    connection = get_connection()

    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    message = {
        "task_id": task_id,
        "model_name": model_name
    }

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message)
    )

    connection.close()