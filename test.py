# from ultralytics import YOLO
#
# model = YOLO("cv-service/app/weights/yolov8n.pt")


import redis

r = redis.Redis(
    host="192.168.233.135",
    port=6379,
    decode_responses=True
)

r.set("test", "hello redis")

value = r.get("test")

print(value)