from cv_app.core.manager import ModelManager
from cv_app.models.task import Task
from cv_app.models.result import Result

from cv_app.utils.oss import upload_file
from cv_app.utils.heatmap import generate_heatmap
import requests
import numpy as np
import time

import cv2
import uuid


def detection(
    db,
    task_id: int,
    model_name: str
):

    # =========================
    # 1. 查询 task
    # =========================
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()
    if not task:
        raise Exception("Task not found")

    image_path = task.image_path

    # =========================
    # 2. 获取模型
    # =========================
    print(model_name)
    model = ModelManager.switch_model(
        model_name
    )
    if model is None:
        raise Exception("Model not found")

    # =========================
    # 3. 模型推理
    # =========================

    response = requests.get(image_path)

    image_array = np.asarray(
        bytearray(response.content),
        dtype=np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    start_time = time.perf_counter()
    results = model(image, save=False)
    end_time = time.perf_counter()
    duration = end_time - start_time  # 单位：秒(float)

    result_list = []

    # =========================
    # 4. 解析 label
    # =========================
    CONFIDENCE_THRESHOLD = 0.5

    for r in results:

        for box in r.boxes:

            confidence = float(box.conf[0])

            if confidence < CONFIDENCE_THRESHOLD:
                continue

            cls_id = int(box.cls[0])

            label = r.names[cls_id]

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            result_list.append({
                "label": label,
                "confidence": round(confidence, 4),
                "x1": round(x1, 2),
                "y1": round(y1, 2),
                "x2": round(x2, 2),
                "y2": round(y2, 2),
            })

    # =========================
    # 5. 生成 bbox 图片
    # =========================
    if len(results) == 0:
        bbox_image = image
    else:
        bbox_image = results[0].plot()

    bbox_filename = f"{uuid.uuid4()}.jpg"

    _, bbox_buffer = cv2.imencode(
        ".jpg",
        bbox_image
    )

    bbox_url = upload_file(
        bbox_buffer.tobytes(),
        bbox_filename
    )

    # =========================
    # 6. 热力图（后面加）
    # =========================
    # 下载原图到内存

    original_image = image
    # image_array = np.asarray(
    #     bytearray(response.content),
    #     dtype=np.uint8
    # )
    #
    # original_image = cv2.imdecode(
    #     image_array,
    #     cv2.IMREAD_COLOR
    # )

    heatmap_image = generate_heatmap(
        original_image,
        results
    )

    heatmap_filename = f"{uuid.uuid4()}.jpg"

    _, heatmap_buffer = cv2.imencode(
        ".jpg",
        heatmap_image
    )

    heatmap_url = upload_file(
        heatmap_buffer.tobytes(),
        heatmap_filename
    )

    # =========================
    # 7. 更新 task
    # =========================
    task.bbox_image = bbox_url

    task.heatmap_image = heatmap_url

    task.status = "CV_success"
    task.cv_model = model_name
    task.cv_duration = round(duration, 4)

    # =========================
    # 8. 写入 result
    # =========================
    for item in result_list:

        result = Result(
            task_id=task.id,
            label=item["label"],
            confidence=item["confidence"],
            x1=item["x1"],
            y1=item["y1"],
            x2=item["x2"],
            y2=item["y2"],
        )

        db.add(result)

    # =========================
    # 9. 提交数据库
    # =========================
    db.commit()

    # =========================
    # 10. 返回
    # =========================
    return {
        "task_id": task.id,
        "bbox_image": bbox_url,
        "heatmap_image": heatmap_url,
        "results": result_list
    }