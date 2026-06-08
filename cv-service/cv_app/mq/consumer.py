import json

from cv_app.mq.rabbit import get_connection

from cv_app.db.database import SessionLocal
from cv_app.mq.producer import send_nlp_task

# 你的YOLO检测函数
from cv_app.services.detect import detection


QUEUE_NAME = "cv_queue"
MAX_RETRY = 3

def callback(ch, method, properties, body):
    data = json.loads(body)
    task_id = data["task_id"]
    model_name = data["model_name"]

    db = SessionLocal()

    try:
        print(f"[CV Worker] task_id: {task_id}")

        detection(db, task_id, model_name)

        print("CV检测完成")

        send_nlp_task(task_id)

        db.commit()

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print("CV ERROR:", e)

        retry_count = data.get("retry", 0)

        if retry_count < 3:
            data["retry"] = retry_count + 1
            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=True
            )
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    finally:
        db.close()


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