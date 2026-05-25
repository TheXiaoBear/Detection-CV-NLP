import json

from app.mq.rabbit import get_connection

from app.db.database import SessionLocal
from app.mq.producer import send_nlp_task

# 你的YOLO检测函数
from app.services.detect import detection


QUEUE_NAME = "cv_queue"
MAX_RETRY = 3

def callback(ch, method, properties, body):

    data = json.loads(body)

    task_id = data["task_id"]

    print(f"[CV Worker] task_id: {task_id}")

    db = SessionLocal()

    try:
        detection(db, task_id)
        print("CV检测已经完成")

        print("NLP检测即将开始")
        send_nlp_task(task_id)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print("CV ERROR:", e)

        retry_count = data.get("retry", 0)

        if retry_count < MAX_RETRY:

            data["retry"] = retry_count + 1

            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=True
            )
        else:
            print("CV failed permanently")
            ch.basic_ack(delivery_tag=method.delivery_tag)
    finally:

        db.close()

        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )


def start_worker():

    connection = get_connection()

    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

    print("[CV Worker] waiting message...")

    channel.start_consuming()