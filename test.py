from ultralytics import YOLO
# https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt
model = YOLO("cv-service/cv_app/weights/yolov11n.pt")


# import redis
#
# r = redis.Redis(
#     host="192.168.233.135",
#     port=6379,
#     decode_responses=True
# )
#
# r.set("test", "hello redis")
#
# value = r.get("test")
#
# print(value)